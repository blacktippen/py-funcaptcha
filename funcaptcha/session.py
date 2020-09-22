from .crypto import aes_encrypt, aes_decrypt
from .profile import Profile
from .challenge import Challenge
from .util import parse_session_token
from io import BytesIO
from PIL import Image
from base64 import b64encode

import os
import urllib3
import urllib.parse
import random
import json
import time
import math
import secrets
import subprocess
import logging

DEBUG = False

## Exceptions
class FuncaptchaError(Exception): pass

## Classes
class Session:
    """
    Initialize the session
    """
    def __init__(self, 
        public_key: str,
        service_url: str,
        profile: Profile,
        proxy_url: str=None,
        manager=None):
        self.public_key = public_key
        self.service_url = service_url
        self.service_host = urllib.parse.urlsplit(service_url)[1]
        self.profile = profile
        self.window = self.profile.window
        self.pool_mgr = manager or urllib3.PoolManager(maxsize=2)
        
        self.tracking = dict()
        self.full_token = None
        self.session_url = None
        self.token = None
        self.region = None
        self.meta = None
        self._get_session()


    """
    Represent the session using it's token
    """
    def __repr__(self):
        return self.token
    

    """
    Generate data necessary for sending requests
    """
    def request(self, reqname, extra={}):
        info = self.profile.request_templates[reqname]
        st = time.time()

        ## prepare url
        url = info["url"].format(
            service_url=self.service_url,
            public_key=self.public_key)

        ## prepare request body
        payload = dict()
        for k, v in info.get("body", {}).items():
            if type(v) != str:
                payload[k] = v
                continue
            payload[k] = v.format(
                bda=self.get_bda(),
                public_key=self.public_key,
                random_float=random.uniform(0,1),
                user_agent=self.profile.user_agent,
                window_url=self.window.url,
                window_url_nopath=f"https://{self.window.domain}",
                session_token=self.token,
                region=self.region,
                **extra
            )
        body = payload and self.profile.url_encode_dict(payload)

        ## prepare headers
        headers = dict()
        for k, v in info["headers"].items():
            headers[k] = v.format(
                service_host=self.service_host,
                window_url_nopath=f"https://{self.window.domain}",
                service_url_nopath=f"https://{self.service_host}",
                user_agent=self.profile.user_agent,
                session_url=self.session_url,
                window_url=self.window.url,
                payload_length=body!=None and len(body),
                timestamp=int(time.time()) * 100000,
                tracking=aes_encrypt(json.dumps(
                    self.tracking \
                        if extra.get("game_type")==1 \
                        else {}, **self.profile.json_settings),
                    f"REQUESTED{self.token}ID")
            )
    
        resp = self.pool_mgr.request(
            method=info["method"],
            url=url,
            headers=headers,
            body=body
        )
        data = json.loads(resp.data)
        if "error" in data:
            raise FuncaptchaError(data["error"])

        if DEBUG:
            print(self.tracking)
            print(f"{info['method']} {url} - Elapsed: {round(time.time()-st, 2)}s")
        return resp

    
    """
    Generate value for bda parameter
    """
    def get_bda(self):
        bda = []
        t = time.time()
        bda.append(dict(
            value="js",
            key="api_type"
        ))
        bda.append(dict(
            value=1,
            key="p"
        ))
        bda.append(dict(
            key="f",
            value=self.profile.fingerprint_hash
        ))
        bda.append(dict(
            key="n",
            value=b64encode(str(int(t)).encode("utf-8")).decode("utf-8")
        ))
        bda.append(dict(
            key="wh",
            value="%s|%s" % (self.window.hash, self.profile.protochain_hash)
        ))
        bda.append(dict(
            key="fe",
            value=self.profile.fe
        ))
        bda.append(dict(
            key="ife_hash",
            value=self.profile.ife_hash
        ))
        bda.append(dict(
            value=1,
            key="cs"
        ))
        bda.append(dict(
            key="jsbd",
            value="{"+self.profile.jsbd.format(
                window_title=self.window.title,
                DOT=random.randint(30,50),
                DMT=random.randint(30,50)
            )+"}"
        ))
        tf = int(t - (t % 21600))
        key = self.profile.user_agent + str(tf)
        bda = json.dumps(bda, **self.profile.json_settings)
        bda = aes_encrypt(bda, key)
        bda = b64encode(bda.encode("utf-8")).decode("utf-8")
        return bda


    """
    Load fresh session data from funcaptcha
    """
    def _get_session(self):
        resp = self.request("get_session")
        data = json.loads(resp.data)

        self.full_token = data["token"]
        self.session_url = f"https://{self.service_host}/fc/gc/?"
        self.session_url += "&".join(
            k[0] + "=" + k[1]
            for k in [x.split("=", 2) for x in ("token="+data["token"]).split("|")])
        pt = parse_session_token(data["token"])
        self.token = pt["token"]
        self.region = pt["r"]
        self.public_key = pt["pk"]
        self.meta = int(pt["meta"])

        self.request("site_url_analytics")


    """
    Create new challenge
    """
    def get_challenge(self, **kw):
        resp = self.request("get_challenge")
        data = json.loads(resp.data)

        return Challenge(self, data, **kw)