from api_keys import spotify_client_id, spotify_client_secret
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
import sys, os
import spotipy
import database_querying as dbq
import requests
import spotipy.util as util
# client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
from json.decoder import JSONDecodeError
import urllib.parse

class User:

    def __init__(self, username):
        # fetch user library
        self.redirect_uri = 'http://localhost/'
        self.scope = 'user-library-read user-playlist-modify'
        self.username = username
        self.token = util.prompt_for_user_token(username = self.username, scope=self.scope, client_id=spotify_client_id,client_secret=spotify_client_secret, redirect_uri=redirect_uri)
        self.tracks = self.get_all_tracks()
        # get audio features and genres for all tracks that don't exist


    def get_track_word_frequencies(self, track):
        word_counts = Counter()
        pids = track['pids']
        total_occurences = len(pids)
        for pid in pids:
            lemmas = dbq.get_playlist_lemmas(pid)['lemmas']
            for lemma in lemmas:
                word_counts[lemma] += 1
        for word in word_counts:
            word_counts[word] /= total_occurences
        return word_counts

    def get_all_tracks(self):
        if self.token:
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_saved_tracks()
            # for item in results['items']:
            #     track = item['track']
            #     print track['name'] + ' - ' + track['artists'][0]['name']
        else:
            print("Can't get token for", username)



import sys
import spotipy
import spotipy.util as util

scope = 'user-playlist-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    sys.exit()
username = 'jeremy_reikes'
redirect_uri = 'http://localhost/'
token = util.prompt_for_user_token(username = 'scope='user-library-read user-playlist-modify', client_id=spotify_client_id,client_secret=spotify_client_secret, redirect_uri=redirect_uri)
# response = requests.get('https://accounts.spotify.com/authorize?client_id=94fdc1a3412a42c5a92897fa57ca94b0&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%2F')

results['next']
