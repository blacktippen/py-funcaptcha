# py-funcaptcha
Python module for interacting with *ArkoseLabs FunCaptcha*. **NOT A SOLVER IN ITSELF.**

Tested on: 2020-06-14

### Things to note
- `<ch>.full_token` is the token you submit to the website once you solved the challenge
- Pillow's *.rotate* method is reversed, therefore you'll have to multiply the degree by -1 to get the correctly rotated image

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
    #proxy="https://127.0.0.1:3128"
    )
    
## Obtain a new challenge
ch = s.create_challenge()

## Print some challenge details
print("Full Token:", ch.full_token)
print("Number of Images:", ch.get_image_count())

## Iterate over challenge images (Pillow)
for image, submit in ch.get_iter():
    ## Generate a random guess
    guess = ch.angle * randint(1, int(360/ch.angle) - 1)
    
    ## Show preview (.rotate method is reversed)
    image.rotate(guess*-1).show()
    
    ## Submit guess
    print("Submitting guess:", guess)
    solved = submit(guess)

## Print final result
print("Solved:", solved)
```

If you have any questions, suggestions or offers, feel free to message me on twitter at [@h0nde](https://twitter.com/h0nde).
