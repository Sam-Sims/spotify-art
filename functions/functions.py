import spotipy
from configparser import ConfigParser

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
    print(response)
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
    print(response)
    list = []
    for i, item in enumerate(response['items']):
        dictOfArtists = {
            "name": item['name'],
            "artist_name": item['artists'][0]['name']
        }
        list.append(dictOfArtists)
    return list
