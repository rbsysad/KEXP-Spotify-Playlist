# REMOVE DUPLICATE TRACKS IN KEXP PLAYLIST

import json

class RemoveDuplicates:

    def __init__(self):
        self.file = {}
        self.data = []
        self.clean_data = []

    def write_to_playlist(self):
        print("---WRITING DE-DUPED PLAYLIST TO FILE---")
        with open('playlist.json', 'w') as writeJSON:
            json.dump(self.clean_data, writeJSON)

    def dedupe(self):
        print("---REMOVING DUPLICATES FROM DATA---")
        self.file = open('playlist.json', 'r')
        self.data = json.load(self.file)

        for song in self.data:
            if song not in self.clean_data:
                self.clean_data.append(song)

        self.write_to_playlist()