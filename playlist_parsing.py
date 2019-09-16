'''
all_tracks:
    _id:
    track_name:
    track_name_lemmas:
    artist_id:
    popularity:
    release_date:
    playlist_ids: list
    audio_features: {'danceability': 0.893,
      'energy': 0.387,
      'key': 6,
      'loudness': -11.96,
      'mode': 0,
      'speechiness': 0.371,
      'acousticness': 0.177,
      'instrumentalness': 4.04e-05,
      'liveness': 0.137,
      'valence': 0.378,
      'tempo': 115.009,
      'duration_ms': 129412,
      'time_signature': 4}
    raw_lyrics: GET IMMEDIATELY AND THEN ADD LEMMAS, ANALYSIS

    tweets:
    lyrics_lemmas:
    lyrical analysis:
        vulgarity:
        positivity:
        negativity:
        neutrality:

parsed_playlists:
    _id:
    data_analyzed:
    track_ids:
    description:
    description_lemmas:
    name:
    name_lemmas:

all_artists:
    _id:
    genres:
    artist_name:
    artist_name_lemmas:

'''



'''  twitter scraping

all_tracks:
    _id:
    track_name:
    track_name_lemmas:
    artist_id:
    popularity:
    release_date:
    playlist_ids: list
    audio_features: {'danceability': 0.893,
      'energy': 0.387,
      'key': 6,
      'loudness': -11.96,
      'mode': 0,
      'speechiness': 0.371,
      'acousticness': 0.177,
      'instrumentalness': 4.04e-05,
      'liveness': 0.137,
      'valence': 0.378,
      'tempo': 115.009,
      'duration_ms': 129412,
      'time_signature': 4}
    raw_lyrics: GET IMMEDIATELY AND THEN ADD LEMMAS, ANALYSIS
    tweets:
    lyrics_lemmas:
    lyrical analysis:
        vulgarity:
        positivity:
        negativity:
        neutrality:

FROM SPOTIFY -
    id
    track_name
    artist_id
    popularity
    release_date
    playlist_ids
    audio_features

FROM GENIUS LYRICS
    Don't get lyrics at start - use as an update - but then when have most lyrics start doing it immediatelyt

parsed_playlists:
    _id:
    data_analyzed:
    track_ids:
    description:
    description_lemmas:
    name:
    name_lemmas:

FROM SPOTIFY -
    id
    date analyzed:
    track_ids
    description
    name


all_artists:
    _id:
    genres:
    artist_name:
    artist_name_lemmas:

FROM SPOTIFY -
    id
    genres
    artist_name
'''

'''
workflow -
    is playlist parsed?
        yes - option to update - not yet
        no - add playlist
            get playlist from spotify
                playlist = sp.user_playlist
                grab user_id
                grab all_tracks


'''

from pymongo import MongoClient
client = MongoClient()
db = client.spotify_db
all_tracks = db.all_tracks
parsed_playlists = db.parsed_playlists
all_artists = db.all_artists
from tqdm import tqdm
from user_playlist_fetching import parse_playlist
from database_querying import *
import csv
path = '/Users/jeremy/Desktop/final_project/data' # use your path
import glob
all_files = glob.glob(path + "/*.csv")

def add_playlist(playlist_id):
    if playlist_exists(playlist_id):
        print(f'{playlist_id} already parsed')
    else:
        parse_playlist(playlist_id)


def build_database(all_files):
    all_pids = set()
    for file in all_files:
        with open(file, 'r') as f:
          reader = csv.reader(f)
          lines = list(reader)
          for line in lines:
              all_pids.add(line[1])
    all_pids.remove('')
    for pid in tqdm(list(all_pids)):
        add_playlist(pid)

build_database(all_files)
