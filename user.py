import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import warnings
import pickle
import tqdm
from collections import Counter, defaultdict
from spacy.lang.en import English
warnings.filterwarnings('ignore')
import time
from api_keys import spotify_client_id, spotify_client_secret
client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
import database_querying as dbq
import pandas as pd
from textblob import TextBlob
import numpy as np
# from pymongo import MongoClient
# client = MongoClient(readPreference='secondary')
# db = client.spotify_db
# tracks_db = db.tracks_db
# playlists_db = db.playlists_db
#
class User:
    def __init__(self, playlist_id):
        self.tids = self.fetch_playlist_tids(playlist_id)
        self.tracks = dbq.get_tracks(self.tids)
        self.data = self.convert_tracks_to_df(self.tracks)

        # self.playlist_word_counts = self.generate_word_counts()

    def fetch_playlist_tids(self, playlist_id):
        playlist = sp.user_playlist(playlist_id=playlist_id, user=None)
        total_tracks = playlist['tracks']['total']
        all_tids = self.get_tids_from_spotify(playlist)
        if total_tracks > 700 or total_tracks == 0 or not all_tids:
            print(f'Unable to parse {playlist_id}')
            return None
        additional_pages = total_tracks // 100
        if total_tracks % 100 == 0:
            additional_pages -= 1
        for i in range(additional_pages):
            playlist = sp.user_playlist_tracks(playlist_id=playlist_id, user=None, offset = (i+1)*100)
            curr_tids = self.get_tids_from_spotify(list)
            all_tids.extend(curr_tids)
        return all_tids

    def get_tids_from_spotify(self, playlist):
        try:
            tids = [track['track']['id'] for track in playlist['tracks']['items']]
        except:
            tids = list()
        return tids

    def rank_songs_by_word(self, word):
        for tid, track_counts in self.counts.items():
            self.data.loc[tid, 'word_frequency'] = track_counts.get(word, 0)
        self.data.sort_values(by='word_frequency', ascending=False, inplace=True)


    def convert_tracks_to_df(self, tracks):
        counts = defaultdict(Counter)
        parsed_tracks = list()
        for track in tracks:
            curr_track = dict(word_frequency = 0)
            for key, val in track.items():
                if key != 'audio_features':
                    curr_track[key] = val
            audio_features = track.get('audio_features', False)
            if audio_features:
                for key, val in audio_features.items():
                    curr_track[key] = val
            try:
                counts[track['_id']] = dbq.get_playlist_word_counts(track['_id'])
            except:
                counts[track['_id']] = None
            parsed_tracks.append(curr_track)
        self.counts = counts
        return pd.DataFrame(parsed_tracks).set_index('_id')


user = User('4QSUc9xaEdl5yLnfvfx2Br')
user.data
user.rank_songs_by_word('summer')
user.data
