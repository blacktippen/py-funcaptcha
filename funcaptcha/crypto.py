from . import __path__ as ROOT_PATH
from . import murmur3
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
import random
import hashlib
import subprocess
import os
import json
import string

with open(os.path.join(ROOT_PATH[0], "fp.js")) as f:
    fps = f.read().strip()

def mm3_hash(fe, mode="node"):
    if mode == "node":
        ife = subprocess.check_output([
            "node", "-e", fps, fe]).decode("UTF-8")
    elif mode == "translation":
        ife = murmur3.murmur3.x64hash128(fe, 38)
    return ife

def aes_encrypt(data: (str, bytes), key: str) -> str:
    data = data + chr(16-len(data)%16)*(16-len(data)%16)

    salt = b"".join(random.choice(string.ascii_lowercase).encode() for x in range(8))
    salted, dx = b"", b""
    while len(salted) < 48:
        dx = hashlib.md5(dx+key.encode()+salt).digest()
        salted += dx

    key = salted[:32]
    iv = salted[32:32+16]
    aes = AES.new(key, AES.MODE_CBC, iv)

    encrypted_data = {"ct": b64encode(aes.encrypt(data.encode())).decode("utf-8"), "iv": iv.hex(), "s": salt.hex()}
    return json.dumps(encrypted_data, separators=(',', ':'))


def aes_decrypt(data: (str, bytes), key: str) -> bytes:
    data = json.loads(data)
    dk = key.encode()+bytes.fromhex(data["s"])

    md5 = [hashlib.md5(dk).digest()]
    result = md5[0]
    for i in range(1, 3+1):
        md5.insert(i, hashlib.md5((md5[i-1]+dk)).digest())
        result += md5[i]

    aes = AES.new(result[:32], AES.MODE_CBC, bytes.fromhex(data["iv"]))
    data = aes.decrypt(b64decode(data["ct"]))
    return data
