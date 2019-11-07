import warnings
warnings.filterwarnings('ignore')
from api_keys import spotify_client_id, spotify_client_secret
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient
client = MongoClient()
db = client.spotify_db
all_tracks = db.all_tracks
parsed_playlists = db.parsed_playlists
all_artists = db.all_artists
parsed_playlists.find_one()

import spacy
from database_querying import *
nlp = spacy.load('en_core_web_sm')
client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
from datetime import datetime
from time import sleep
from nlp_helpers import lemmatize
useless_features = ['type', 'uri', 'track_href', 'analysis_url', 'id']

def parse_playlist(playlist_id):
    playlist_complete = True
    if playlist_id == '' or playlist_id == None:
        return None
    try:
        results = sp.user_playlist(playlist_id = playlist_id, user=None)
    except:
        print(f'cant get playlist {playlist_id}')
        return None
    description = results['description']
    name = results['name']

    owner = results['owner']['id']
    total_tracks = results['tracks']['total']

    desc_doc = nlp(description)
    desc_lemmas = lemmatize(desc_doc)
    name_doc = nlp(name)
    name_lemmas = lemmatize(name_doc)
    if total_tracks < 10 or total_tracks > 1000 or desc_doc.lang_ != 'en' or name_doc.lang_ != 'en':
        return None
        print(f'too many or little tracks or not english {playlist_id}')
    playlist_tracks = dict()
    tracks = results['tracks']
    for track in tracks['items']:
        try:
            tid = track['track']['id']
            playlist_tracks[tid] = track
        except:
            print('song ID not present')
    while tracks['next']:
        tracks = sp.next(tracks)
        for track in tracks['items']:
            try:
                tid = track['track']['id']
                playlist_tracks[tid] = track
            except:
                print('song id not present')

    playlist_tids = list()
    tracks_to_add = list()
    artists_to_add = set()

    for tid, track in playlist_tracks.items():
        if not track_exists(tid):
            try:
                track_data = initialize_track(track, playlist_id)
            except:
                continue
            artist_id = track_data['artist_id']
            if not artist_exists(artist_id):
                artists_to_add.add(artist_id)
            tracks_to_add.append(track_data)
        else:
            playlist_tids.append(tid)
            all_tracks.update_one({'_id': tid}, {'$push': {'pids': playlist_id}})
    today = str(datetime.now())[:10]
    skip = False
    tracks_to_add = add_audio_features(tracks_to_add, skip)

    playlist_to_add = dict(_id=playlist_id, name=name, name_lemmas=name_lemmas, owner=owner,
                           date_analyzed=today, description=description, description_lemmas = desc_lemmas, tids=list())
    artists_to_add = list(artists_to_add)
    artists_to_add = add_genres(artists_to_add, skip)

    if skip:
        return # this means there was a local track that screwed things up
    if artists_to_add:
        all_artists.insert_many(artists_to_add)
    if tracks_to_add:
        try:
            all_tracks.insert_many(tracks_to_add)
            for track in tracks_to_add:
                playlist_to_add['tids'].append(track['_id'])
        except:
            print('cannot insert tracks')
            return None
    for tid in playlist_tids:
        playlist_to_add['tids'].append(tid)
    parsed_playlists.insert_one(playlist_to_add)


def add_audio_features(tracks_to_add, skip, skip_local_songs=True):
    tids = [track['_id'] for track in tracks_to_add]
    for i in range((len(tids) // 50) + 1):
        offset = i*50
        curr_ids = get_curr_ids(tids, offset)
        if len(curr_ids) == 0:
            break
        try:
            audio_features = sp.audio_features(curr_ids)
        except:
            if skip_local_songs:
                skip=True
                return None
            audio_features = list()
            for curr_id in curr_ids:
                try:
                    curr_feature = sp.audio_features(curr_id)
                    audio_features.extend(curr_feature)
                except:
                    audio_features.append({})
        for index, curr_features in enumerate(audio_features):
            if curr_features:
                for feature in useless_features:
                    del curr_features[feature]
                tracks_to_add[offset + index - 1]['audio_features'] = curr_features
    return tracks_to_add

def initialize_track(track, playlist_id):
    track_data = dict()
    track_info = track['track']
    track_data['name'] = track_info['name']
    track_data['name_lemmas'] = lemmatize(nlp(track_data['name']))
    track_data['_id'] = track_info['id']
    track_data['popularity'] = track_info['popularity']
    track_data['explicit'] = track_info['explicit']
    track_data['duration'] = track_info['duration_ms']
    track_data['artist_id'] = track_info['artists'][0]['id']
    track_data['pids'] = list([playlist_id])
    return track_data


def add_genres(artist_ids, skip, skip_local_songs=True):
    artists_data = list()
    for i in range((len(artist_ids) // 50) + 1):
        offset = i*50
        curr_ids = get_curr_ids(artist_ids, offset)
        if len(curr_ids) == 0: # in case it's a multiple of 50
            break
        try:
            curr_artists = sp.artists(artist_ids)['artists']
        except:
            if skip_local_songs:
                skip = True
                return None
            curr_artists = list()
            for curr_id in curr_ids:
                try:
                    curr_artist = sp.artist(curr_id)
                    curr_artists.append(curr_artist)
                except:
                    curr_artists.append({})
        for index, curr_artist in enumerate(curr_artists):
            artist_data = dict()
            if not curr_artist:
                artist_data['_id'] = curr_ids[index]
            else:
                artist_data['_id'] = curr_ids[index]
                artist_data['name'] = curr_artist['name']
                artist_data['popularity'] = curr_artist['popularity']
                artist_data['genres'] = curr_artist['genres']
            artists_data.append(artist_data)
    return artists_data

def get_curr_ids(tids, offset):
    try:
        curr_ids = tids[offset:offset+50]
    except:
        curr_ids = tids[offset:]
    return curr_ids