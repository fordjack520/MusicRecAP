import re
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import creds

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret))

inp = input("Input URL: ")

rec_url = re.search("(?P<url>https?://[^\s]+)", inp).group("url")

return_url = requests.get(rec_url).url

item = {}

print(return_url)

if "album" in return_url:
    album = sp.album(return_url)
    item["type"] = album["album_type"]
elif "track" in return_url:
    track = sp.track(return_url)
    item["track_name"] = track["name"]
    album = track["album"]
    item["type"] = track["type"]
    print(f"This song is \"{item['track_name']}\"")
else:
    print("Invalid input.")

item["album_name"] = album["name"]
item["album_artist"] = album["artists"][0]["name"]
item["year"] = album["release_date"][0:4]
item["number_of_tracks"] = album["total_tracks"]

if item["type"] == "track":
    duration = track["duration_ms"]
else:
    duration = 0
    for t in album["tracks"]["items"]:
        duration += t["duration_ms"]

duration_sec = divmod(duration, 1000)[0]
duration_min, duration_sec = divmod(duration_sec, 60)
item["duration"] = f"{duration_min}:{duration_sec}"

print (f'This album is {item["album_name"]} ({item["year"]}) by {item["album_artist"]}. It contains {item["number_of_tracks"]} tracks and runs for {item["duration"]}.')
print (f'This is a(n) {item["type"]}.')

#print(item)