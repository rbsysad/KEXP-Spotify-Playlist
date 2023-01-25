import requests
import json
from shadow import spotify_user_id
from refresh import Refresh


class FindTracks:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.data = ""
        self.spotify_uris = ""
        self.current_artist = ""
        self.current_track = ""
        self.playlist_id = "14s72tOhEexZDSg28Ony2I"

    def search_for_track(self, track_name):
        # Search Spotify for track name, add to csv

        print("---SEARCHING FOR TRACK---")
        limit = 10
        query = "https://api.spotify.com/v1/search?q={}&limit={}&type=track&market=US".format(
            track_name, limit)

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        print(response)
        return response.json()

    def call_refresh(self):
        # Refresh access token

        print("---REFRESHING TOKEN---")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()

    def import_json(self):
        # Import artist/track json, extract track name and artist

        print("---IMPORTING FROM FILE---")

        with open('./data.txt', 'r') as file:
            self.data = file.read()

        print(self.data)
        data_json = json.loads(self.data)

        for i in data_json:
            self.current_artist = i["artist"]
            self.current_track = i["track"]
            self.choose_correct_track(self.search_for_track(i["track"]))

    def choose_correct_track(self, response_json):
        for i in response_json["tracks"]["items"]:
            for j in i["artists"]:
                if j["name"] == self.current_artist:
                    print("---ADDING TRACK URI---")
                    print("{} - {}".format(self.current_artist, self.current_track))
                    self.spotify_uris += i["uri"] + ","
                    self.write_to_file()
                    break

            break

    def write_to_file(self):

        print("---WRITING TO FILE---")
        file = open("uris.txt", "a")
        file.write(self.spotify_uris)
        file.close()

    def add_to_playlist(self):

        print("---IMPORTING URIS FROM FILE---")

        with open('uris.txt', 'r') as file:
            self.spotify_uris = file.read()

        print(self.spotify_uris)

        print("---ADDING TO PLAYLIST---")

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.playlist_id, self.spotify_uris)

        response = requests.post(query, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer {}".format(self.spotify_token)})

        print(response.json())


a = FindTracks()
a.call_refresh()
a.import_json()
