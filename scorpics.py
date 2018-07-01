import json
from pathlib import Path
from urllib.request import urlretrieve

library = dict()

ignore_terms = [
    "Chill Hits",
    "Sweet Soul Sunday",
    "Spotify & Chill",
    "Novidades ",
    "Novedades ",
    "New Music Friday ",
]

def should_ignore(name):
    for term in ignore_terms:
        if term in name:
            return True
    return False

for playlist_json in sorted(Path("json").glob("drake*.json")):
    print("Processing", playlist_json.name)
    n_added = 0
    with playlist_json.open() as f:
        playlists = json.load(f)
        for playlist in playlists["playlists"]["items"]:
            name = playlist["name"]
            if name not in library and not should_ignore(name):
                library[name] = playlist
                n_added += 1
    if n_added == 0:
        playlist_json.unlink()
    print("  Added {} playlists".format(n_added))

print("Total playlists:", len(library))

Path("img").mkdir(exist_ok=True)

for name, playlist in sorted(library.items()):
    fname = "img/" + name + ".jpg"
    if not Path(fname).exists():
        urlretrieve(playlist["images"][0]["url"], fname)
        print(name, "downloaded from" , playlist["images"][0]["url"])

