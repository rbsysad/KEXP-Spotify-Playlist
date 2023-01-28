import requests
import json
from shadow import spotify_user_id, playlist_id
from refresh import Refresh

class KEXPSpotify:

    def __init__(self):
        self.user_id = spotify_user_id
        self.playlist_id = playlist_id
        self.token = ""
        self.artist = ""
        self.track = ""
        self.track_list = []
        self.kexp_endpoint = "https://api.kexp.org/v1/play"

    def call_refresh(self):
    # REFRESH API ACCESS TOKEN
        print("---REFRESHING TOKEN---")
        refreshCaller = Refresh()
        self.token = refreshCaller.refresh()

    def get_songs(self):
    # GET LIST OF SONGS FROM KEXP    
        print("---GETTING SONGS---")
        response = requests.get('https://api.kexp.org/v1/play/')
        response_json = (response.json())
        with open("file.txt") as file:
            for item in response_json['results']:
                # if isinstance(item['artist'], dict):
                #   if isinstance(item['track'], dict):
                #     self.artist = item['artist']['name']
                #     self.track = item['track']['name']
                # self.track_list.append(f"{self.artist} {self.track}")
                file.write()
        file.close()

        print(self.track_list)
        
    def search_for_song(self):
    # ADD SONGS TO SPOTIFY PLAYLIST
    
            for song in self.track_list:
                print(f"---SEARCHING FOR {song}---")
                print()
                query = f"https://api.spotify.com/v1/search?q={song}&limit=1&type=track&market=US"
                response = requests.get(query, headers={"Content-Type": "application/json",
                                                    "Authorization": f"Bearer {self.token}"})

                response_json = response.json()

                