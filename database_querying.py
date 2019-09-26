from pymongo import MongoClient
client = MongoClient(readPreference='secondary')
db = client.spotify_db
all_tracks = db.all_tracks
parsed_playlists = db.parsed_playlists
all_artists = db.all_artists
from collections import Counter
import numpy as np
parsed_playlists.find_one()

''' PLAYLIST FUNCTIONS '''

def playlist_exists(pid):
    return parsed_playlists.count_documents({'_id': pid}, limit = 1) == 1

def get_playlist(pid):
    return parsed_playlists.find_one({'_id': pid})

def get_playlist_lemmas(pid):
    return parsed_playlists.find_one({'_id': pid}, {'name_lemmas': 1})

''' TRACK FUNCTIONS '''

def track_exists(tid):
    return all_tracks.count_documents({'_id': tid}, limit = 1) == 1

def get_track(tid):
    return all_tracks.find_one({'_id': tid})


''' ARTIST FUNCTIONS '''

def artist_exists(aid):
    return all_artists.count_documents({'_id': aid}, limit = 1) == 1

def get_artist(aid):
    return all_artists.find_one({'_id': aid})
# all_tracks.find_one()

# 705310 tracks


# frequencies = get_frequencies_for_word('girls')
# # vals = frequencies.values()
# df = pd.DataFrame(frequencies.values())
# df.hist()
#
# plt.hist(new)
# df = df.apply(np.log)
# df.hist()
from sklearn.preprocessing import StandardScaler
from scipy.stats import boxcox
#
# scaler = StandardScaler()
# df = scaler.fit_transform(df)
# plt.hist(df)
# df.columns = ['values']
# %matplotlib inline
# import pandas as pd
# px.histogram(df)
# import plotly.express as px
# frequencies.most_common()[-20:]
# d
