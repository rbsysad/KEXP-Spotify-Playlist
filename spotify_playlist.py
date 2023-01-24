import requests
import json

playlist_id = "5cWWTWsgNBvu3qL3GrEWJA"
search_endpoint_url = "https://api.spotify.com/v1/search?"
playlist_endpoint_url = "https://api.spotify.com/v1/playlists/5cWWTWsgNBvu3qL3GrEWJA/tracks"

limit = 10
market = "US"
artist = "Aesop Rock"
track = "None Shall Pass"
type = "track"


track_uri_list = []

query = f'{search_endpoint_url}limit={limit}&market={market}&q={track}&type={type}'

response = requests.get(query,
                        headers={"Content-Type": "application/json",
                                 "Authorization": "Bearer "})

json_response = response.json()

print(json_response)


def add_song_to_list(json_response):
    for response in json_response['tracks']['items']:
        for i in response['artists']:
            if i['name'] == artist:
                track_uri_list.append(response['uri'])
                return


# def add_song_to_playlist():
#     response = requests.post(url=playlist_endpoint_url, uris="spotify:track:207jvv3SLF6CGhVW2gOanq", headers={"Content-Type": "application/json",
#                                                                                                               "Authorization": "Bearer BQACCs3B1J5T9biODQv-v7t5xSD9FY3L7yco39x2YUNr2A0op4kBsKAlpuaOG4VQhAWb5VJz6Xrn-epnKGKp2riZtY9z7aYA0ZVcBKhXpM0nS26Y5eqUEROoznRje45VwLbKpQsJTbQDXezwpgYmALDN4JWSouCFsw_f8lKJMNBGXfp26GA7IdcKz1cJaVRnFmcljnsEicuuArouZ5nu"})
#     print(response)


add_song_to_list(json_response)

# add_song_to_playlist()

print(track_uri_list)
