import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from tqdm import tqdm
tqdm.pandas()
from collections import Counter, defaultdict

from pymongo import MongoClient
client = MongoClient(readPreference='secondary')
spotify_db = client.spotify_db
tracks_db = spotify_db.all_tracks
playlists_db = spotify_db.parsed_playlists
artists_db = spotify_db.parsed_playlists

''' TRACK METHODS '''

'''  PLAYLIST METHODS '''

def track_exists(tid):
    return tracks_db.count_documents({'_id': tid}, limit=1) == 1

def playlist_exists(pid):
    return playlists_db.count_documents({'_id': pid}, limit=1) == 1

def artist_exists(aid):
    return artists_db.count_documents({'_id': aid}, limit=1) == 1
