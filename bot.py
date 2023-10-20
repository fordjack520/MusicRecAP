import re
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import creds

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret))

inp = input("Input URL: ")

rec_url = re.search("(?P<url>https?://[^\s]+)", inp).group("url")

return_url = requests.get(rec_url).url

# print(return_url)

if "album" in return_url:
    album = sp.album(return_url)
    item_type = album["album_type"]
elif "track" in return_url:
    track = sp.track(return_url)
    track_name = track["name"]
    album = track["album"]
    item_type = track["type"]
    print(f"This song is \"{track_name}\"")
else:
    print("Invalid input.")

album_name = album["name"]
album_artist = album["artists"][0]["name"]
album_yr = album["release_date"][0:4]
album_tracks = album["total_tracks"]

if item_type == "track":
    duration = track["duration_ms"]
else:
    duration = 0
    for item in album["tracks"]["items"]:
        duration += item["duration_ms"]

duration_sec = divmod(duration, 1000)[0]
duration_min, duration_sec = divmod(duration_sec, 60)
duration_time = f"{duration_min}:{duration_sec}"

print (f"This album is {album_name} ({album_yr}) by {album_artist}. It contains {album_tracks} tracks and runs for {duration_time}.")
print (f"This is a(n) {item_type}.")