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
            "artist_name": item['artists'][0]['name'],
            "popularity": item['popularity'],
            "track_id": item["id"]
        }
        list.append(dictOfArtists)
    print(list)
    return list

def get_visulisation_values(token):
    sp = spotipy.Spotify(auth=token)
    top_tracks = get_user_top_tracks(token, "long_term")
    features = [] # Create empty list to store the song features, as spotipy reeturns a dict within a single element list
    for i, item in enumerate(top_tracks):
        features = features + sp.audio_features(item['track_id']) # Join each list of audio features into one list as tracks looped through
        features[0]["track"] = item['name'] # Add track name as that isnt returned by spotify API
    return features # Returns a list of dictionarys containing audio features for each track

