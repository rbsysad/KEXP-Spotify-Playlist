import json

file = open('playlist.json', 'r')
data = json.load(file)
clean_list = []

for song in data:
    if song not in clean_list:
        clean_list.append(song)

with open('new_playlist.json', 'w') as writeJSON:
    json.dump(clean_list, writeJSON)
