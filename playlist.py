import requests
import json

# TODO: Add support for special characters in track name

offset = 20
song_list = []

while offset <= 10000:
    URL = f'https://api.kexp.org/v1/play?offset={offset}'

    def get_results(URL):
        response = requests.get(URL)
        data = response.json()
        return data['results']

    results = get_results(URL)

    for result in results:
        try:
            artist = (result['artist']['name'])
            track = (result['track']['name'])
            new_dict = {'artist': artist, 'track': track}
            song_list.append(new_dict)
        except:
            continue

    offset += 20
    print(offset, len(song_list))

file = open('playlist.json', 'w')
file.write(json.dumps(song_list))
