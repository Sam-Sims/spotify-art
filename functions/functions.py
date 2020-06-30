import spotipy
from configparser import ConfigParser
import statistics
from io import StringIO, BytesIO

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
                "bpm": items['tempo']
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
    bpm = []
    for i, item in enumerate(features):
        danceability.append(item["danceability"])
        energy.append(item["energy"])
        music_key.append(item['key'])
        popularity.append(item['popularity'])
        valence.append(item['valence'])
        inst.append(item['instrumentalness'])
        mode.append(item['mode'])
        bpm.append(item['bpm'])
    dict_of_avr = {
        "dance": statistics.mean(danceability),
        "energy": statistics.mean(energy),
        "key": statistics.mode(music_key),
        "popularity": statistics.mean(popularity),
        "valence": statistics.mean(valence),
        "inst": statistics.mean(inst),
        "mode": statistics.mode(mode),
        "bpm": statistics.mean(bpm)
    }
    return dict_of_avr

def evaluate(averages):
    if averages['mode'] == 0:
        sky = "night"
    else:
        sky = "day"

    if averages['bpm'] < 90:
        forest = "sparse"
    elif 90 < averages['bpm'] < 120:
        forest = "medium"
    elif averages['bpm'] > 120:
        forest = 'dense'

    if averages['popularity'] < 40:
        balloons = "sparse"
    elif 40 < averages['bpm'] < 65:
        balloons = "medium"
    elif averages['bpm'] > 65:
        balloons = 'dense'

    if averages['energy'] < 0.5:
        mountain = "red"
    elif averages['energy'] > 0.5:
        mountain = "blue"

    evaluation = {
        "sky": sky,
        "forest": forest,
        "balloons": balloons,
        "mountain" : mountain,
        "popularity": averages['popularity']
    }
    return evaluation

def serve_img(img):
    img_io = BytesIO()
    img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return img_io

def construct_report(evaluation):
    report_string = "This is an image dynamically generated using your spotify listening habbits. "
    if evaluation['sky'] == "day":
        key = "major"
    elif evaluation['sky'] == "night":
        key = "minor"
    background_string = f"It is {evaluation['sky']}time out representing that the majority of your top songs are in the {key} key. \n"
    report_string = report_string + background_string

    if evaluation['forest'] == "sparse":
        forest_explained = "is lower than 90 BPM "
    elif evaluation['forest'] == "medium":
        forest_explained = "falls between 91 and 120 BPM "
    elif evaluation['forest'] == "dense":
        forest_explained = "is greater than 120 BPM "
    forest_string = f"The forest is of {evaluation['forest']} thickness because the average BPM of your top songs {forest_explained}. "
    report_string = report_string + forest_string

    if evaluation['balloons'] == "sparse":
        balloon_explained = "a few  "
    elif evaluation['balloons'] == "medium":
        balloon_explained = "some  "
    elif evaluation['balloons'] == "dense":
        balloon_explained = "a large number "
    balloon_string = f"There are {balloon_explained} balloons which represent the the fact that the average popularity of your top tracks is {evaluation['popularity']} percent. "
    report_string = report_string + balloon_string

    if evaluation['mountain'] == "red":
        mountain_explained = "high  "
    elif evaluation['mountain'] == "blue":
        mountain_explained = "low  "
    mountain_string = f"The mountain is {evaluation['mountain']} because of the {mountain_explained} energy of your top tracks. "
    report_string = report_string + mountain_string
    return report_string
