# py-funcaptcha
Python module for interacting with *ArkoseLabs FunCaptcha*. **NOT A SOLVER IN ITSELF.**

### Things to note
- `<ch>.full_token` is the token you submit to the website once you solved the challenge
- Pillow's *.rotate* method is reversed, therefore you'll have to multiply the degree by -1 to get the correctly rotated image

## If ArkoseLabs is starting to detect the module as a bot, try the following things:
- Change some stuff in `jsbd`
- Change user agent

### Setup
```bash
sudo apt install nodejs
pip3 install -r requirements.txt
```
On Windows machines you'll also have to install the module `pycryptodome`


### Usage
```python
from py_funcaptcha import FunCaptchaSession
from random import randint

## Create session for Roblox's login endpoint
s = FunCaptchaSession(
    public_key="9F35E182-C93C-EBCC-A31D-CF8ED317B996",
    service_url="https://roblox-api.arkoselabs.com",
    page_url="https://www.roblox.com/login",
    #proxy="https://127.0.0.1:8888",
    predownload_images=True)
## Obtain challenge
ch = s.create_new_challenge()

## Print challenge details
print("Full Token:", ch.full_token)
print("Number of Images:", len(ch.image_urls))

## Iterate over challenge images
## (the image is PIL.Image object)
for image, submit in ch.get_iter():
    ## Generate random guess
    ## (this is not a viable option for solving challenges, as in a real scenario you would use machine-learning or human-assisted image rotating services)
    guess = ch.angle * randint(1, int(360/ch.angle) - 1)
    
    ## Show preview (.rotate method is reversed)
    image.rotate(guess*-1).show()
    
    ## Submit guess
    solved = submit(guess)

## Print final result
print("Solved:", solved)
```

If you have any questions, suggestions or offers, feel free to message me on twitter at [@h0nde](https://twitter.com/h0nde).
