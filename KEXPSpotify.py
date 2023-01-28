import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred


class KEXPSpotify:

    def __init__(self):
        self.user_id = cred.spotify_user_id
        self.playlist_id = cred.playlist_id
        self.artist = ""
        self.track = ""
        self.track_list = []
        self.kexp_endpoint = "https://api.kexp.org/v1/play"
        self.spotify = ""
        self.uri_list = []

    def spotify_authorization(self):
        # AUTHORIZE USING SPOTIPY

        print("---AUTHORIZING---")

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=cred.client_ID,
            client_secret=cred.client_SECRET,
            redirect_uri=cred.redirect_url,
            scope=cred.scope))

        print(self.spotify)

    def get_kexp_songs(self):
        # GET LIST OF SONGS FROM KEXP

        print("---GETTING KEXP SONGS---")
        response = requests.get('https://api.kexp.org/v1/play/')
        response_json = (response.json())
        for item in response_json['results']:
            if isinstance(item['artist'], dict):
                if isinstance(item['track'], dict):
                    self.artist = item['artist']['name']
                    self.track = item['track']['name']

                    formatted_artist = self.artist
                    formatted_track = self.track
                    formatted_string = "track:{} artist:{}".format(formatted_track, formatted_artist)
                    self.track_list.append(formatted_string)

        print(self.track_list)

    def get_wtmd_songs(self):
        # GET LIST OF SONGS FROM WTMD

        print("---GETTING WTMD SONGS---")
        response = requests.get

    def search_spotify(self):
        # SEARCH SPOTIFY FOR SONGS
        # RETURNS SPOTIFY URI

        for song in self.track_list:
            print(f"---SEARCHING FOR {song}---")
            print()

            q = str(song)
            results = self.spotify.search(q, limit=1, offset=0, market="US")

            for item in results["tracks"]["items"]:
                self.uri_list.append(item["uri"])

    def add_to_playlist(self):
        print("---ADDING SONGS TO PLAYLIST---")
        self.spotify.playlist_add_items(self.playlist_id, self.uri_list, position=None)

