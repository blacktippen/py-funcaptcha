# py-funcaptcha
Python3 wrapper for `ArkoseLabs FunCaptcha`'s client with precise browser request emulation, and support for gametype 1 and 3.

# Things to note
- The `manager` parameter of `Session` requires a `urllib3.PoolManager` or `urllib3.ProxyManager` object, you can learn more about it [here](https://urllib3.readthedocs.io/en/latest/advanced-usage.html)
- Solving more than one challenge per session is not recommended, instead try re-using `PoolManager` objects for optimized performance
- `session.full_token` is the token you'll submit to your target website
- Solving and submitting tokens with the same IP address is necessary on most websites

# GameType 3 Example
```python
from funcaptcha import Session, load_profiles, tile_num_to_location
from urllib3 import PoolManager, ProxyManager

profiles = load_profiles("./profiles/roblox-signup")

s = Session(
    public_key="9F35E182-C93C-EBCC-A31D-CF8ED317B996",
    service_url="https://roblox-api.arkoselabs.com",
    profile=profiles[0].new(),
    manager=ProxyManager("http://localhost:8888")
)
ch = s.get_challenge()

if ch.game_type != 3:
    exit(f"Game type 3 was expected, received type {ch.game_type}")

for im in ch.images(pil=True):
    ## display challenge image
    im.show()
    ## wait for user input
    num = int(input("tile num: ")) -1
    ## calculate "click" location based on tile number
    loc = tile_num_to_location(num)
    ## submit guess
    ch.check_answer(loc)

print("Solved:", ch.solved)
print("Took:", ch.elapsed())
```

# Profiles
Profiles and profile instances are one of the main features of this module. Their purpose is to emulate the behaviour of browsers and devices.

Configuration files for profiles are written in YAML, and can be loaded using `load_profiles` by specifying the directory as the first parameter.

Profile instances can be created by calling `.new()` on a `Profile` object.

# Utilities
You can import additional utilities from the module like so:
```python
from funcaptcha import tile_num_to_location
```

## load_profiles(path: str)
Loads profiles from directory of configs

## tile_num_to_location(tile_num: int) [for game-type 3]
Returns [X,Y] location according to tile_num (starts at 0)

## slice_tiles(im: PIL.Image) [for game-type 3]
Returns sliced tiles from image
