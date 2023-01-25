# SEARCH SPOTIFY FOR TRACK AND ADD TO PLAYLIST

import requests
import json
from shadow import spotify_user_id, playlist_id
from refresh import Refresh

class FindTracks:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.data = ""
        self.spotify_uri = ""
        self.current_artist = ""
        self.current_track = ""
        self.playlist_id = playlist_id
        self.base_url = "https://api.spotify.com/v1/"

    def search_for_track(self, track_name):
        # CALL SEARCH GET API ENDPOINT FOR TRACK
            
        print(f"---SEARCHING FOR TRACK: {self.current_artist} - {self.current_track} ---")
        limit = 5
        query = "https://api.spotify.com/v1/search?q={}&limit={}&type=track&market=US".format(
            track_name, limit)
    
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                                 "Authorization": f"Bearer {self.spotify_token}"})
        print(str(response.status_code) + "\n")
        return response.json()

    def call_refresh(self):
        # REFRESH API ACCESS TOKEN

        print("---REFRESHING TOKEN---")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()

    def import_json(self):
        # IMPORT DATA FROM FILE

        print("---IMPORTING FROM FILE---")

        with open('playlist.json', 'r') as file:
            self.data = file.read()

        data_json = json.loads(self.data)

        for i in data_json:
            self.current_artist = i["artist"]
            self.current_track = i["track"]
            self.choose_correct_track(self.search_for_track(i["track"]))

    def choose_correct_track(self, response_json):
        # FILTER SEARCH RESULTS FOR MATCHING ARTIST
        try: 
            for i in response_json["tracks"]["items"]:
                for j in i["artists"]:
                    if j["name"] == self.current_artist:
                        print("---ADDING TRACK URI---")
                        print("{} - {}".format(self.current_artist,
                            self.current_track), "\n")
                        self.spotify_uri = i["uri"]
                        self.add_to_playlist()
                        self.write_to_file()
                        break
                break
        except: print("ERROR", "\n")

    def write_to_file(self):
        # STORE SUCCESSFUL TRACK ADDITIONS IN JSON FORMAT

        print("---WRITING TO FILE---\n")
        file = open("success.json", "a")
        file.write("'artist': '{}', 'track:' '{}'".format(self.current_artist, self.current_track))
        file.close()

    def add_to_playlist(self):
        # CALL PLAYLIST POST API ENDPOINT, ADD TRACK

        print("---ADDING TO PLAYLIST---")

        query = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks?uris={self.spotify_uri}"

        response = requests.post(query, headers={"Content-Type": "application/json",
                                                 "Authorization": f"Bearer {self.spotify_token}"})

        print(response.json(), "\n")
