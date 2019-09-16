from pymongo import MongoClient
client = MongoClient(readPreference='secondary')
db = client.spotify_db
all_tracks = db.all_tracks
parsed_playlists = db.parsed_playlists
all_artists = db.all_artists


''' PLAYLIST FUNCTIONS '''

def playlist_exists(pid):
    return parsed_playlists.count_documents({'_id': pid}, limit = 1) == 1

def get_playlist(pid):
    return parsed_playlists.find_one({'_id': pid})


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
