# spotify-art

This is a project aimed at visulising your spotify data. Developed using flask and python for the spotify API calls. The p5js library was used for the visulisation.

## Deployment

The website can be found at https://spotify-flask.onrender.com/

## Installation

To install the webserver locally, download, install requirements and run app.py

API keys must be generated from spotify (https://developer.spotify.com)
Client and secret keys can then either be set in the env variables, or entered into the config file.
(If the latter, uncomment the code reading the config file)
```bash
pip install -r requirements.txt
```

## Visulisation
The visulisation is done using the p5js javascript library. 

**API Workflow:**

User logs into spotify -> get top 20 tracks -> for each track get: key, energy, bpm and danceability -> average each value
