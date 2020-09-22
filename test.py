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