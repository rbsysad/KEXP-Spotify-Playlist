import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import cred
from spinitron.client import Spinitron

class KEXPSpotify:

    def __init__(self):
        self.user_id = cred.spotify_user_id
        self.kexp_playlist_id = cred.kexp_playlist_id
        self.wtmd_playlist_id = cred.wtmd_playlist_id
        self.artist = ""
        self.track = ""
        self.track_list = []
        self.kexp_endpoint = "https://api.kexp.org/v1/play"
        self.spotify = ""
        self.uri_list = []
        self.temp_track_list = []

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

                    formatted_string = "track:{} artist:{}".format(self.track, self.artist)
                    self.track_list.append(formatted_string)

        print(self.track_list)

    def get_wtmd_songs(self):
        # GET LIST OF SONGS FROM WTMD
        print("---GETTING WTMD SONGS---")

        wtmd_url = "https://wtmdradio.org/playlist/dynamic/RecentSongs.html"
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

        driver = webdriver.Firefox(profile, executable_path="venv/bin/geckodriver", options=opts)

        driver.get(wtmd_url)

        sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        p_list = soup.find_all("p")
        for p in p_list:
            amazon_url = (p.find("a").attrs["href"])
            song_string = amazon_url[104:]
            song = song_string.split("+")
            self.track = song[0]
            self.artist = song[1]
            formatted_string = "track:{} artist:{}".format(self.track, self.artist)
            self.temp_track_list.append(formatted_string)
            if len(self.temp_track_list) == 95:
                self.track_list.append(self.temp_track_list)
                self.temp_track_list = []

    def get_wknc_songs(self):
        # GET LIST OF SONGS FROM WKNC
        print("---GETTING WKNC SONGS---")

        wknc_url = "https://spinitron.com/WKNC/"
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

        driver = webdriver.Firefox(profile, executable_path="venv/bin/geckodriver", options=opts)

        driver.get(wknc_url)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        tr_list = soup.find_all("tr", {"class": "spin-item"})

        for item in tr_list:
            print(item.attrs)
        #
        # for tr in tr_list:
        #     song_list.append([tr])
        #
        # song_list = song_list[1:]
        # for item in song_list:
        #     for item2 in item:
        #         self.track_list.append(item2.text[21:])

    def search_spotify(self):
        # SEARCH SPOTIFY FOR SONGS
        # RETURNS SPOTIFY URI

        for temp_track_list in self.track_list:
            for song in temp_track_list:
                print(f"---SEARCHING FOR {song}---")
                print()

                q = song
                results = self.spotify.search(q, limit=1, offset=0, market="US")

                for item in results["tracks"]["items"]:
                    self.uri_list.append(item["uri"])
            self.add_to_playlist()

    def add_to_playlist(self):
        print("---ADDING SONGS TO PLAYLIST---")
        self.spotify.playlist_add_items(self.wtmd_playlist_id, self.uri_list, position=None)
        self.uri_list = []
