import random

def parse_session_token(token):
    return {v[0]: v[1] for v in [v.split("=", 2) for v in ("token="+token).split("|")]}

def get_imageset(url):
    imageset = url.split("production/")[1].split("/")[0] \
                if "production/" in url else None
    return imageset

def tile_num_to_location(sn, offset=25):
    second_row = sn > 2
    if second_row:
        sn -= 3
    sr = [
        sn*100,
        100 if second_row else 0
    ]
    return [
        random.randint(sr[0]+offset, (sr[0]+100)-offset),
        random.randint(sr[1]+offset, (sr[1]+100)-offset)
    ]

def slice_tiles(im, size=100, offset=3):
    for yr in range(int(im.size[1]/size)):
        for xr in range(int(im.size[0]/size)):
            yield im.crop((
                (xr * size) + offset,
                (yr * size) + offset,
                ((xr+1) * size) - offset,
                ((yr+1) * size) - offset
            ))

def get_xy() -> list:
    start_pos = [117, 248]
    button_size = [90, 28]
    new_pos = [
        start_pos[0] + random.randint(1, button_size[0]),
        start_pos[1] + random.randint(1, button_size[1])]
    return new_pos