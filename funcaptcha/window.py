import urllib.parse
import secrets

class Window:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.domain = urllib.parse.urlsplit(url)[1]
        self.hash = secrets.token_hex(16)