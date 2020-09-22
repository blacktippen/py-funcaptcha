from .crypto import aes_encrypt, aes_decrypt
from .util import get_xy

from PIL import Image
from io import BytesIO
from base64 import b64decode
import json
import time
import math

## Globals
API_BREAKERS = {
    "default": lambda c: dict(px="%.2f"%(c[0]/300), py="%.2f"%(c[1]/200), x=c[0], y=c[1]),
    "method_1": lambda c: dict(x=c[1],y=c[0]),
    "method_2": lambda c: dict(x=c[1],y=(c[1]+c[0])*c[0]),
    "method_3": lambda c: dict(a=c[0],b=c[1]),
    "method_4": lambda c: [c[0],c[1]],
    "method_5": lambda c: list(map(math.sqrt, [c[1],c[0]])),
}
DEFAULT_DEGREE = 18.00

## Classes
class Challenge:
    """
    Initialize the challenge based on the data argument
    """
    def __init__(self, session, data, setup=True, preload_images=False):
        self.session = session
        self.profile = self.session.profile
        self.token = data["challengeID"]
        self.game_type = data["game_data"]["gameType"]
        self.game_variant = data["game_data"].get("game_variant")
        self.waves = data["game_data"]["waves"]
        self.image_urls = data["game_data"]["customGUI"]["_challenge_imgs"]
        self.image_cache = {}
        self.api_breaker = data["game_data"]["customGUI"].get("api_breaker")
        self.answer_history = []
        self.solved = None
        self.created = time.time()
        self.preload_images = preload_images

        if self.game_type == 1:
            self.rdegree = None
            if "_guiFontColr" in data["game_data"]["customGUI"]:
                self.rdegree = float(int(data["game_data"]["customGUI"]["_guiFontColr"].replace("#", "")[-3:], 16))
                if self.rdegree and self.rdegree > 113: self.rdegree = self.rdegree/10
            if not self.rdegree or self.rdegree >= 360:
                self.rdegree = DEFAULT_DEGREE

        if preload_images:
            for url in self.image_urls:
                self.image_cache[url] = self.download(url)

        if setup:
            self.setup()


    """
    Finish setting up the challenge
    """
    def setup(self):
        self.image_cache = {url: self.download(url) for url in self.image_urls} \
            if self.preload_images else self.image_cache
        self.request("game_loaded_analytics")
        if self.game_type == 1:
            self.session.tracking["sc"] = get_xy()
        self.get_encryption_key()
        self.request("user_clicked_verify_analytics")


    """
    Returns elapsed seconds since challenge was created, for debugging
    """
    def elapsed(self):
        return round(time.time()-self.created, 2)


    """
    Repres-ent challenge in format of `{challenge_token} ({session_token})`
    """
    def __repr__(self):
        return self.token


    """
    Wrapper for session's .request method, sends challenge data
    """
    def request(self, reqname, extra={}):
        return self.session.request(reqname, dict(
            challenge_token=self.token,
            game_type=self.game_type,
            game_variant=self.game_variant,
            **extra
        ))
    

    """
    Get initial encryption key for images
    """
    def get_encryption_key(self):
        resp = self.request("get_encryption_key")
        data = json.loads(resp.data)
        self.decryption_key = data["decryption_key"]

    
    """
    Submit guess
    """
    def check_answer(self, answer=None):
        if answer:
            self.answer_history.append(answer)
            if self.game_type == 1:
                self.session.tracking["dc"] = get_xy()
                if len(self.answer_history) == self.waves:
                    self.session.tracking["ech"] = "%.2f" % answer

        if self.game_type == 1:
            answer_str = ",".join(list(map("{:.2f}".format, self.answer_history)))

        elif self.game_type == 3:
            answer_str = json.dumps(list(map(
                API_BREAKERS[self.api_breaker or "default"],
                self.answer_history)), **self.profile.json_settings)

        resp = self.request("check_answer", dict(
            answer=aes_encrypt(answer_str, self.session.token)))
        data = json.loads(resp.data)
        self.decryption_key = data.get("decryption_key")
        self.solved = data.get("solved")
        return data.get("solved")


    """
    Download image using provided :url argument
    """
    def download(self, url):
        resp = self.session.pool_mgr.request("GET", url)
        im = resp.data
        return im


    """
    Iterate over images
    """
    def images(self, pil=True):
        for im_url in self.image_urls:
            if not im_url in self.image_cache:
                im = self.download(im_url)
            else:
                im = self.image_cache[im_url]
                del self.image_cache[im_url]
            try:
                im = aes_decrypt(im, self.decryption_key)
            except: pass
            try:
                im = b64decode(im)
            except: pass
            if pil:
                im = Image.open(BytesIO(im))
            yield im