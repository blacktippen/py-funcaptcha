## py_funcaptcha
## https://github.com/davidbaszucki/py-funcaptcha
## Updated: 2020-06-18
## Contact: @h0nde


import requests
import random
import time
import httpagentparser
from urllib.parse import urlsplit
from requests.packages.urllib3.exceptions import InsecureRequestWarning
## For image manipulation
from PIL import Image
from io import BytesIO
## Modules for encryption and decryption
import mmh3
from Crypto.Cipher import AES
import base64
import hashlib
import json
import execjs
import string
import re
import secrets

with open("fp.js") as f:
    mm3js = execjs.compile(f.read())

## Default params
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
]

## Root encryption keys for certain endpoints
keys = {
    "setupChallenge": "e1195fb20c24c57fe10b6344e491712c9", ## message(G9ii).N2r
    "checkAnswer": "e7f17dfd538950feb86db852866355fd4", ## self(G9ii).k3R(325)
    "getEncryptionKey": "e0845bd2f28b346f17342add88380d5f7", ## Z6K(G9ii).k3R(617)
    "keepAlive": "ef010a06aced43965476da87e88d5cebc", ## t6K(G9ii).k3R(128)
    "sendAnalytics": "ea5367c13f2c947113d7b9690968846fd", ## node(G9ii).k3R(565)
}

## Query keys for certain endpoints
param_keys = {
    "setupChallenge": "ed166c47957e04fb333d6176d0f5bdcd4",
    "checkAnswer": "e655b8492aa3fa2a4d470d4dd152e2ed2",
    "getEncryptionKey": "e5c0abde3c09cdd7042d2eba69739fe8d",
    "keepAlive": "e07d86bcac2e4e5a3b18750a4bc13fe1f",
    "sendAnalytics": "e3083a3db8645f38d1b2cfa0ad264a276"
}


## Create dict of fields from full token string
def parse_full_token(token: str) -> dict:
    token = "token=" + token
    assoc = {}

    for field in token.split("|"):
        s = field.partition("=")
        key, value = s[0], s[-1]
        assoc[key] = value
    
    return assoc


## Get random float value
def get_float() -> float:
    return random.uniform(0, 1)


## Get random X,Y click coordinates for button
def get_xy() -> list:
    start_pos = [117, 248]
    button_size = [90, 28]
    new_pos = [
        start_pos[0] + random.randint(1, button_size[0]),
        start_pos[1] + random.randint(1, button_size[1])]
    return new_pos


## Get browser name from user agent
def get_browser_name(user_agent) -> str:
    browser_name = httpagentparser.detect(user_agent)["browser"]["name"].lower().strip()
    return browser_name


## Get random user agent for session
def get_random_user_agent() -> str:
    return random.choice(USER_AGENTS)


## Custom timestamp format used by FC
def get_timestamp() -> str:
    ts = str(int(time.time() * 1000))
    p1 = ts[:7]
    p2 = ts[7:13]
    n = p1 + "00" + p2
    return n


## Generate canvas fingerprint
def get_canvas_fingerprint(browser: str) -> int:
    return random.randint(121058022, 124058022)


## Generate font keys
def get_font_keys(browser: str) -> list:
    if browser == "chrome":
        return "Arial,Arial Black,Arial Narrow,Book Antiqua,Bookman Old Style,Calibri,Cambria,Cambria Math,Century,Century Gothic,Century Schoolbook,Comic Sans MS,Consolas,Courier,Courier New,Garamond,Georgia,Helvetica,Impact,Lucida Bright,Lucida Calligraphy,Lucida Console,Lucida Fax,Lucida Handwriting,Lucida Sans,Lucida Sans Typewriter,Lucida Sans Unicode,Microsoft Sans Serif,Monotype Corsiva,MS Gothic,MS PGothic,MS Reference Sans Serif,MS Sans Serif,MS Serif,Palatino Linotype,Segoe Print,Segoe Script,Segoe UI,Segoe UI Light,Segoe UI Semibold,Segoe UI Symbol,Tahoma,Times,Times New Roman,Trebuchet MS,Verdana,Wingdings,Wingdings 2,Wingdings 3".split(",")
    
    elif browser == "firefox":
        return "Arial,Arial Black,Arial Narrow,Arial Rounded MT Bold,Book Antiqua,Bookman Old Style,Calibri,Cambria,Cambria Math,Century,Century Gothic,Century Schoolbook,Comic Sans MS,Consolas,Courier,Courier New,Garamond,Georgia,Helvetica,Impact,Lucida Bright,Lucida Calligraphy,Lucida Console,Lucida Fax,Lucida Handwriting,Lucida Sans,Lucida Sans Typewriter,Lucida Sans Unicode,Microsoft Sans Serif,Monotype Corsiva,MS Gothic,MS Outlook,MS PGothic,MS Reference Sans Serif,MS Sans Serif,MS Serif,Palatino Linotype,Segoe Print,Segoe Script,Segoe UI,Segoe UI Light,Segoe UI Semibold,Segoe UI Symbol,Tahoma,Times,Times New Roman,Trebuchet MS,Verdana,Wingdings,Wingdings 2,Wingdings 3".split(",")


## Generate plugin keys
def get_plugin_keys(browser: str) -> list:
    if browser == "firefox":
        return []
    
    elif browser == "chrome":
        return "Chrome PDF Plugin,Chrome PDF Viewer,Native Client".split(",")


## Generate window protochain hash (unique for every browser/version)
def get_window_protochain_hash(browser: str) -> str:
    if browser == "chrome":
        return "5d76839801bc5904a4f12f1731a7b6d1"
       
    elif browser == "firefox":
        return "8987e63ab78ec35fa6c5ebc6bb515fac"


## Generate JSBD data
## HL = history.length; NCE = Cookies enabled; DO = Orientation-related something
def get_jsbd(browser: str) -> str:
    if browser == "chrome":
        return json.dumps({
            "HL": random.randint(2, 3),
            "NCE": True,
            "DA": None,
            "DR": None,
            "DMT": random.randint(30, 38),
            "DO": None,
            "DOT": random.randint(28, 51)
        }, separators=(',',':'))
    
    elif browser == "firefox":
        return json.dumps({
            "HL": 3,
            "NCE": True,
            "DMTO": 1,
            "DOTO": 1
        }, separators=(',',':'))
    
    
## Calculate angle from _guiFontColr
def get_rotation_angle(font_clr: str) -> float:
    angle = int(font_clr.replace("#", "")[-3:], 16)
    if angle > 113:
        angle = angle/10
    return float(angle)


## CryptoJS AES Encryption
def cryptojs_encrypt(data: (str, bytes), key: str) -> str:
    # Padding
    data = data + chr(16-len(data)%16)*(16-len(data)%16)

    salt = b"".join(random.choice(string.ascii_lowercase).encode() for x in range(8))
    salted, dx = b"", b""
    while len(salted) < 48:
        dx = hashlib.md5(dx+key.encode()+salt).digest()
        salted += dx

    key = salted[:32]
    iv = salted[32:32+16]
    aes = AES.new(key, AES.MODE_CBC, iv)

    encrypted_data = {"ct": base64.b64encode(aes.encrypt(data.encode())).decode("utf-8"), "iv": iv.hex(), "s": salt.hex()}
    return json.dumps(encrypted_data, separators=(',', ':'))


## CryptoJS AES Decryption
def cryptojs_decrypt(data: (str, bytes), key: str) -> bytes:
    data = json.loads(data)
    dk = key.encode()+bytes.fromhex(data["s"])

    md5 = [hashlib.md5(dk).digest()]
    result = md5[0]
    for i in range(1, 3+1):
        md5.insert(i, hashlib.md5((md5[i-1]+dk)).digest())
        result += md5[i]
    
    aes = AES.new(result[:32], AES.MODE_CBC, bytes.fromhex(data["iv"]))
    data = aes.decrypt(base64.b64decode(data["ct"]))
    return data


class FunCaptchaChallenge():
    images = None
    metadata = {}
    
    ## Set up challenge object
    def __init__(self, session: str, bda: str, full_token: str,
                 session_token: str, region: str, lang: str, analytics_tier: str,
                 scl: (None, int)):
        self.session = session
        self.scl = scl
        self.proxy = self.session.proxy
        self.bda = bda
        self.full_token = full_token
        self.session_token = session_token
        self.region = region
        self.lang = lang
        self.analytics_tier = analytics_tier
        self.send_analytics(render_type="canvas", sid=self.region, category="Site URL", analytics_tier=self.analytics_tier, session_token=self.session_token, action=self.session.page_url)
        self.reload(status="init")

    
    def encrypt_query(self, data, source):
        ## calculate key for root
        key = "secure" + keys[source] + "mode"

        ## calculate key for the inner data
        if source == "setupChallenge":
            data_key = "init" + self.session_token + "key"

        elif source == "sendAnalytics":
            data_key = "analytical" + self.session_token + "key"

        elif source == "checkAnswer":
            data_key = "cat" + self.session_token + "key"

        elif source == "getEncryptionKey":
            data_key = "timed" + self.session_token + "key"

        elif source == "keepAlive":
            data_key = "rekey" + self.session_token + "key"
        
        data_key = "secure" + data_key + "mode"

        d = cryptojs_encrypt(json.dumps({
            "token": self.session_token,
            "data": cryptojs_encrypt(json.dumps(data), data_key)
        }), key)

        return {param_keys[source]: d}


    def decrypt_resp(self, data, source):
        if source == "setupChallenge":
            key = "init_return" + self.session_token
        
        elif source == "checkAnswer":
            key = "ca_reply" + self.session_token
        
        elif source == "getEncryptionKey":
            key = "ekey_reply" + self.session_token

        d = cryptojs_decrypt(data, key) \
            .rpartition(b"}")[0] + b"}"
        return json.loads(d)
    

    ## Reload the challenge
    def reload(self, status: str):
        ts = get_timestamp()
        r = self.session.r.get(
            url=f"{self.session.service_url}/fc/gc/?token=" + self.full_token.replace("|", "&"),
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cache-control": "no-cache",
                **self.session.get_additional_browser_headers(),
                "Upgrade-Insecure-Requests": "1",
                "Referer": self.session.service_url + "/fc/gc/?token=" + self.full_token.replace("|", "&")})

        if self.scl:
            data = {
                "token": self.session_token,
                "sid": self.region,
                "analytics_tier": self.analytics_tier,
                "lang": self.lang,
                "data": {"status": status},
                "render_type": "canvas",
                "id_sec_cl": self.session_token
            }
        else:
            data = {
                "analytics_tier": self.analytics_tier,
                "render_type": "canvas",
                "lang": self.lang,
                "sid": self.region,
                "token": self.session_token,
                "data[status]": status}
            
        if self.scl:
            data = self.encrypt_query(data, "setupChallenge")

        r_resp = self.session.r.post(
            url=f"{self.session.service_url}/fc/gfct/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "X-NewRelic-Timestamp": ts,
                "X-Requested-With": "XMLHttpRequest",
                "X-Requested-ID": self.get_request_id(),
                **self.session.get_additional_browser_headers(),
                "Origin": self.session.service_url, 
                "Referer": self.session.service_url + "/fc/gc/?token=" + self.full_token.replace("|", "&")},
            cookies={
                "timestamp": ts},
            data=data)
        
        if self.scl:
            r_resp = self.decrypt_resp(r_resp.text, "setupChallenge")
        
        else:
            r_resp = r_resp.json()

        self.metadata = {}
        self.token = r_resp["challengeID"]
        self.id = r_resp["challengeURL"]
        self.timeout = r_resp["sec"]
        self.angle = get_rotation_angle(r_resp["game_data"]["customGUI"]["_guiFontColr"])
        self.encrypted_mode = bool(r_resp["game_data"]["customGUI"]["encrypted_mode"])
        self.image_urls = r_resp["game_data"]["customGUI"]["_challenge_imgs"]

        if self.image_urls:
            ## Preload images
            if self.session.predownload_images:
                self.images = list(map(self.download_image, self.image_urls))
            
            self.send_analytics(render_type="canvas", sid=self.region, category="loaded", game_token=self.token, analytics_tier=self.analytics_tier, game_type=1, session_token=self.session_token, action="game loaded")
    
            ## Get encryption key, if needed
            if self.encrypted_mode:
                self.key = self.get_encryption_key()
                self.send_analytics(render_type="canvas", sid=self.region, category="begin app", game_token=self.token, analytics_tier=self.analytics_tier, game_type=1, session_token=self.session_token, action="user clicked verify")
    

    ## Return image count
    def get_image_count(self) -> int:
        return len(self.image_urls)


    ## This is some sort of weird metadata that's sent in
    ## the X-Requested-ID header
    def update_metadata(self, origin: str, value=None):
        if origin == "ekey" and not self.metadata.get("sc"):
            self.metadata["sc"] = get_xy()
        
        elif origin == "guess" and not self.metadata.get("dc"):
            self.metadata["dc"] = get_xy()
        
        elif origin == "lastguess" and value:
            self.metadata["ech"] = "{:.2f}".format(value)
    
    
    ## Send analytics logging request
    def send_analytics(self, **kwargs) -> bool:
        ts = get_timestamp()
        data = {**kwargs}
        if self.scl:
            data = self.encrypt_query(data, "sendAnalytics")
        an_resp = self.session.r.post(
            url=f"{self.session.service_url}/fc/a/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cache-control": "no-cache",
                "X-NewRelic-Timestamp": ts,
                "X-Requested-With": "XMLHttpRequest",
                "X-Requested-ID": self.get_request_id(),
                **self.session.get_additional_browser_headers(),
                "Origin": self.session.service_url, 
                "Referer": self.session.service_url + "/fc/gc"},
            cookies={
                "timestamp": ts},
            data=data)
        
        if self.scl:
            an_resp = {"logged": True} ##self.decrypt_resp(an_resp.text, "sendAnalytics")
        else:
            an_resp = an_resp.json()

        return an_resp.get("logged")
    

    ## Submit guesses
    def submit_guesses(self, guesses: list) -> (bool, None):
        data = ",".join(map("{:.2f}".format, guesses))
        encrypted_data = cryptojs_encrypt(data, self.session_token)

        self.update_metadata(origin="guess")
        if len(guesses) == len(self.image_urls):
            self.update_metadata(origin="lastguess", value=guesses[-1])

        if self.scl:
            data = {
                "sid": self.region,
                "session_token": self.session_token,
                "game_token": self.token,
                "guess": encrypted_data,
                "analytics_tier": self.analytics_tier,
                "sec_id": self.session_token}
        else:
            data = {
                "game_token": self.token,
                "session_token": self.session_token,
                "sid": self.region,
                "guess": encrypted_data,
                "analytics_tier": self.analytics_tier}
        
        if self.scl:
            data = self.encrypt_query(data, "checkAnswer")
        
        ts = get_timestamp()
        sg_resp = self.session.r.post(
            url=f"{self.session.service_url}/fc/ca/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cache-control": "no-cache",
                "X-NewRelic-Timestamp": ts,
                "X-Requested-With": "XMLHttpRequest",
                "X-Requested-ID": self.get_request_id(),
                **self.session.get_additional_browser_headers(),
                "Origin": self.session.service_url, 
                "Referer": self.session.service_url + "/fc/gc"},
            cookies={
                "timestamp": ts},
            data=data)

        if self.scl:
            sg_resp = self.decrypt_resp(sg_resp.json()["data"], "checkAnswer")
        else:
            sg_resp = sg_resp.json()
        
        ## Update encryption key if response contains one
        if "decryption_key" in sg_resp:
            self.key = sg_resp["decryption_key"]
        
        ## Return status of challenge
        return sg_resp.get("solved")


    ## Download image data from url
    def download_image(self, image_url: str) -> bytes:
        i_resp = self.session.r.get(
            url=image_url,
            headers={
                "Referer": f"{self.session.service_url}/fc/apps/canvas/{self.id}/?meta=6"})
        return i_resp.content
    

    ## Get encryption key for the first image
    def get_encryption_key(self) -> str:
        self.update_metadata(origin="ekey")

        data = {
                "game_token": self.token,
                "sid": self.region,
                "session_token": self.session_token}
        
        if self.scl:
            data = self.encrypt_query(data, "getEncryptionKey")

        ts = get_timestamp()
        ek_resp = self.session.r.post(
            url=f"{self.session.service_url}/fc/ekey/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cache-control": "no-cache",
                "X-NewRelic-Timestamp": ts,
                "X-Requested-With": "XMLHttpRequest",
                "X-Requested-ID": self.get_request_id(),
                **self.session.get_additional_browser_headers(),
                "Origin": self.session.service_url, 
                "Referer": f"{self.session.service_url}/fc/gc"},
            cookies={
                "timestamp": ts},
            data=data)
        
        if self.scl:
            ek_resp = self.decrypt_resp(ek_resp.json()["data"], "getEncryptionKey")
        else:
            ek_resp = ek_resp.json()
        
        return ek_resp["decryption_key"]
    

    ## Generates value for X-Requested-ID header
    def get_request_id(self) -> str:
        key = "REQUESTED" + self.session_token + "ID"
        data = json.dumps(self.metadata, separators=(',', ':'))
        return cryptojs_encrypt(data, key)


    def get_iter(self):
        guesses = []
        images_enabled = self.session.predownload_images
        for img_data in self.images or self.image_urls:
            if not images_enabled:
                img_data = self.download_image(img_data)
            img_data = cryptojs_decrypt(img_data, self.key)
            img = Image.open(BytesIO(img_data))
            def submit(guess):
                guesses.append(guess)
                return self.submit_guesses(guesses)
            yield img, submit


class FunCaptchaSession:
    ## Set up session object
    def __init__(self,
            public_key: str,
            service_url: str,
            page_url: str,
            user_agent: (str, None) = None,
            proxy: (str, None) = None,
            predownload_images: bool = True,
            verify: bool = True,
            timeout: int = 15):

        if not user_agent:
            user_agent = get_random_user_agent()

        self.public_key = public_key
        self.service_url = service_url.rstrip("/")
        self.page_url = page_url.rstrip("/")
        self.site_url = "https://" + urlsplit(self.page_url).netloc
        self.user_agent = user_agent
        self.browser = get_browser_name(self.user_agent)
        self.predownload_images = predownload_images

        ## Create and set-up requests.Session() object
        self.r = requests.session()
        self.proxy = proxy
        if proxy: self.r.proxies = {"http": proxy, "https": proxy}
        self.r.timeout = timeout
        self.r.headers["User-Agent"] = self.user_agent
        self.r.headers["Accept"] = "*/*"
        self.r.headers["Accept-Language"] = "en-US,en;q=0.9"
        self.r.headers["Accept-Encoding"] = "gzip, deflate, br"

        ## Disable SSL validation (for debugging)
        if not verify:
            self.r.verify = False
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    

    ## Get base64-encoded JSON string of browser data for identification
    def get_browser_data(self) -> str:
        data = []

        ## Fingerprint
        fonts = get_font_keys(self.browser)
        plugins = get_plugin_keys(self.browser)
        canvas_fp = get_canvas_fingerprint(self.browser)

        fe = [
            ## DoNotTrack flag
            "DNT:" + ("unspecified" if self.browser == "firefox" else "unknown"),
            ## Language
            "L:en-US",
            ## Depth
            "D:24",
            ## Pixel ratio
            "PR:1",
            ## Screen resolution
            "S:1920,1080",
            ## Available screen resolution (browser window size)
            "AS:1920,1040",
            ## Time offset
            "TO:-120",
            ## Session storage enabled
            "SS:true",
            ## Local storage enabled
            "LS:true",
            ## Indexed DB enabled
            "IDB:true",
            ## .addBehaviour enabled - https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/ms535922(v%3Dvs.85)
            "B:false",
            ## OpenDB enabled
            "ODB:" + ("true" if self.browser == "chrome" else "false"),
            ## CPU class
            "CPUC:unknown",
            ## Platform key
            "PK:Win32",
            ## Canvas fingerprint
            "CFP:" + str(canvas_fp),
            ## Has fake resolution
            "FR:false",
            ## Has fake OS
            "FOS:false",
            ## Has fake browser
            "FB:false",
            ## Javascript fonts
            "JSF:" + ",".join(fonts),
            ## Plugin keys
            "P:" + ",".join(plugins),
            ## Touch
            "T:0,false,false",
            ## navigator.hardwareConcurrency value
            "H:8",
            ## Flash enabled
            "SWF:false"]
        
        ## Calculate hashes
        ## I haven't managed to replicate fp hashes yet, so it's just filled with a random value for now
        fp = secrets.token_hex(16)
        ife_hash = mm3js.call("x64hash128", ", ".join(fe), 38)

        ## Window hash + Window protochain
        wh = secrets.token_hex(16) + "|" + get_window_protochain_hash(self.browser)
        
        ## Generate JSBD
        jsbd = get_jsbd(self.browser)
        ts = time.time()
        
        ## BDA Data
        data.append({"key": "api_type", "value": "js"})
        data.append({"value": 1, "key": "p"})
        data.append({"key": "f", "value": fp})
        data.append({"key": "n", "value": base64.b64encode(str(int(ts)).encode("utf-8")).decode("utf-8")})
        data.append({"key": "wh", "value": wh})
        data.append({"value": fe, "key": "fe"})
        data.append({"key": "ife_hash", "value": ife_hash})
        data.append({"value": 1, "key": "cs"})
        data.append({"key": "jsbd", "value": jsbd})
    
        ## Calculate encryption key
        timeframe = int(ts - (ts % 21600))
        key = self.user_agent + str(timeframe)

        ## JSON -> AES -> BASE64
        data = json.dumps(data, separators=(',', ':'))
        data = cryptojs_encrypt(data, key)
        data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        return data


    ## Browsers often have unique headers of their own. This function
    ## aims to include those headers depending on the user agent.
    def get_additional_browser_headers(self, dirx="same-origin") -> dict:
        if self.browser == "chrome":
            return {
                "Sec-Fetch-Site": dirx,
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty"}
        
        elif self.browser == "firefox":
            return {
                "TE": "Trailers"}
        
        return {}


    ## Get new challenge
    def create_challenge(self) -> FunCaptchaChallenge:
        bda = self.get_browser_data()
        rnd = get_float()
        nc_resp = self.r.post(
            url=f"{self.service_url}/fc/gt2/public_key/{self.public_key}",
            headers={
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": self.site_url,
                **self.get_additional_browser_headers("cross-site"),
                "Referer": self.page_url},
            data={
                "bda": bda,
                "public_key": self.public_key,
                "site": self.site_url,
                "userbrowser": self.user_agent,
                "simulate_rate_limit": 0,
                "simulated": 0,
                "language": "en",
                "rnd": rnd}).json()
        

        ## Create FunCaptchaChallenge object based on data
        ## returned by /fc/gc/public_key/{pk}
        full_token = nc_resp["token"]
        data = parse_full_token(full_token)
        return FunCaptchaChallenge(
            session=self,
            bda=bda,
            full_token=full_token,
            session_token=data["token"],
            region=data["r"],
            lang=data["lang"],
            analytics_tier=int(data["at"]),
            scl="scl" in data and int(data["scl"]))
