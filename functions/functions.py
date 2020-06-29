import spotipy
from configparser import ConfigParser
import statistics

class Config:
    def __init__(self):
        config = ConfigParser()
        config.read('./api_key.ini')
        print('Config Loaded!')
        #  LastFM config
        self.secret_id = config.get('SPOTIFY_API_CONFIGURATION', 'secret')
        self.client_id = config.get('SPOTIFY_API_CONFIGURATION', 'client')


def get_user_top_artists(token, range):
    sp = spotipy.Spotify(auth=token)
    response = sp.current_user_top_artists(limit=20, time_range=range)
    list = []
    for i, item in enumerate(response['items']):
        dictOfArtists = {
            "name": item['name'],
            "popularity": item['popularity']
        }
        list.append(dictOfArtists)
    return list

def get_user_top_tracks(token, range):
    sp = spotipy.Spotify(auth=token)
    response = sp.current_user_top_tracks(limit=20, time_range=range)
    list = []
    for i, item in enumerate(response['items']):
        dictOfArtists = {
            "name": item['name'],
            "artist_name": item['artists'][0]['name'],
            "popularity": item['popularity'],
            "track_id": item["id"]
        }
        list.append(dictOfArtists)
    return list

def get_visulisation_values(token):
    sp = spotipy.Spotify(auth=token)
    top_tracks = get_user_top_tracks(token, "long_term")
    list_of_values = []
    for i, item in enumerate(top_tracks):
        features = sp.audio_features(item['track_id']) # Join each list of audio features into one list as tracks looped through
        track_name = item['name']
        artist_name = item['artist_name']
        popularity = item['popularity']
        for j, items in enumerate(features):
            dict_of_values = {
                "name": track_name,
                "artist_name": artist_name,
                "popularity": popularity,
                "danceability": items['danceability'],
                "energy": items['energy'],
                "mode": items['mode'],
                "instrumentalness": items['instrumentalness'],
                "valence": items['valence'],
                "key": items['key'],
            }
            list_of_values.append(dict_of_values)
    return list_of_values # Returns a list of dictionarys containing audio features for each track


def average_features(features):
    danceability = []
    energy = []
    music_key = []
    popularity = []
    valence = []
    inst = []
    mode = []
    for i, item in enumerate(features):
        danceability.append(item["danceability"])
        energy.append(item["energy"])
        music_key.append(item['key'])
        popularity.append(item['popularity'])
        valence.append(item['valence'])
        inst.append(item['instrumentalness'])
        mode.append(item['mode'])
    dict_of_avr = {
        "dance": statistics.mean(danceability),
        "energy": statistics.mean(energy),
        "key": statistics.mode(music_key),
        "popularity": statistics.mean(popularity),
        "valence": statistics.mean(valence),
        "inst": statistics.mean(inst),
        "mode": statistics.mode(mode)
    }
    print(dict_of_avr)
