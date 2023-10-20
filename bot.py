import re
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import creds

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret))

inp = input("Input URL: ")

rec_url = re.search("(?P<url>https?://[^\s]+)", inp).group("url")

return_url = requests.get(rec_url).url

print(return_url)

if "album" in return_url:
    album = sp.album(return_url)
elif "track" in return_url:
    track = sp.track(return_url)
    track_name = track["name"]
    album = track["album"]
    print(f"This song is \"{track_name}\"")
else:
    print("Invalid input.")

album_name = album["name"]
album_artist = album["artists"][0]["name"]
album_yr = album["release_date"][0:4]
print (f"This album is {album_name} ({album_yr}) by {album_artist}")