from .window import Window
from .crypto import mm3_hash

import subprocess
import urllib.parse
import random
import time
import secrets
import os
import glob
import yaml

def load_profiles(path="./profiles"):
    profiles = []
    for fp in glob.glob(os.path.join(path, "*.yaml")):
        with open(fp, "rb") as f:
            profiles.append(Profile(yaml.safe_load(f)))
    return profiles

## Classes
class Profile:
    """
    Initialize profile based on the data argument
    """
    def __init__(self, data):
        self.data = data

    """
    Create a new profile instance based on current profile
    """
    def new(self):
        return ProfileInstance(Window(**self.data["window"]), self.data)


class ProfileInstance:
    """
    Initialize profile instance based on provided window and data argument
    """
    def __init__(self, window, data):
        self.name = data["name"]
        self.user_agent = data["user_agent"]
        self.url_encoding_map = data.get("url_encoding_map")
        self.request_templates = data["requests"]
        self.json_settings = data["json_settings"]
        self.protochain_hash = data["protochain_hash"]
        self.fingerprint_hash = secrets.token_hex(16)
        self.jsbd = data["jsbd"]
        self.window = window
        self.fe = list()
        for f in data["fe"]:
            self.fe.append(f.format(
                timezone_offset=60 * random.randint(-6, 6),
                canvas_fingerprint=random.randint(-234234235, 345345223)
            ))
        self._ife_hash = None
    
    @property
    def ife_hash(self):
        self._ife_hash = self._ife_hash or \
            mm3_hash(", ".join(self.fe))
        return self._ife_hash

    def url_encode_dict(self, d):
        if self.url_encoding_map:
            def t(tx, d):
                for k,v in d.items():
                    tx = tx.replace(k, v)
                return tx
            return "&".join([
                "%s=%s" % (t(str(k), self.url_encoding_map), t(str(v), self.url_encoding_map))
                for k,v in d.items()
            ]).replace("Site%20URL", "Site+URL")
        return urllib.parse.urlencode(d)