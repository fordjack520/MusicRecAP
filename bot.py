import os
import re
import spotipy
import requests

from spotipy.oauth2 import SpotifyClientCredentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

import creds

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = creds.spreadsheet_id

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret))

def main():

    inp = input("Input URL: ")

    rec_url = re.search("(?P<url>https?://[^\s]+)", inp).group("url")

    return_url = requests.get(rec_url, timeout=3.05).url

    item = {}

    # print(return_url)

    if "album" in return_url:
        album = sp.album(return_url)
        item["type"] = album["album_type"]
        item["name"] = album["name"]
    elif "track" in return_url:
        track = sp.track(return_url)
        item["name"] = track["name"]
        album = track["album"]
        item["type"] = track["type"]
        #print(f"This song is \"{item['name']}\"")
    else:
        print("Invalid input.")

    item["album_name"] = album["name"]
    item["album_artist"] = album["artists"][0]["name"]
    item["year"] = int(album["release_date"][0:4])
    item["number_of_tracks"] = album["total_tracks"]
    item["genre"] = None

    if item["type"] == "track":
        duration = track["duration_ms"]
    else:
        duration = 0
        for t in album["tracks"]["items"]:
            duration += t["duration_ms"]

    duration_sec = divmod(duration, 1000)[0]
    duration_min, duration_sec = divmod(duration_sec, 60)
    item["duration"] = f"{duration_min:02}:{duration_sec:02}"

    #print (f'This album is {item["album_name"]} ({item["year"]}) by {item["album_artist"]}. It contains {item["number_of_tracks"]} tracks and runs for {item["duration"]}.')
    #print (f'This is a(n) {item["type"]}.')

    #print(item)

    try:
        service = getService()
        sheet = service.spreadsheets()
        
        values = [[item["type"], item["name"], item["album_artist"], item["year"], item["duration"], item["genre"], rec_url]]

        body = {'values': values}
        result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range="main!A2",valueInputOption="RAW", body=body).execute()

    except HttpError as error:
        print(error)

def getService():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
        
    return build("sheets", "v4", credentials=credentials)

if __name__ == "__main__":
    main()