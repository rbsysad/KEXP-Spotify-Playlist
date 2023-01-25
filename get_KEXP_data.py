# CALL KEXP PLAYLIST GET API ENDPOINT FOR TRACKS PLAYED

import requests
import json
from remove_duplicates import RemoveDuplicates

class GetKEXPData:

    def __init__(self):
        self.offset = 20
        self.song_list = []
        self.URL = f'https://api.kexp.org/v1/play?offset={self.offset}'

    def get_results(self):
        response = requests.get(self.URL)
        data = response.json()
        return data['results']

    def parse_results(self, results):
        print("---GETTING KEXP PLAYLIST DATA---")
        while self.offset < 40:
            for result in results:
                try:
                    artist = (result['artist']['name'])
                    track = (result['track']['name'])
                    new_dict = {'artist': artist, 'track': track}
                    self.song_list.append(new_dict)
                except:
                    continue
            self.offset += 20

    def write_to_playlist(self):
        print("---WRITING KEXP DATA TO FILE---")
        file = open('playlist.json', 'w')
        file.write(json.dumps(self.song_list))

