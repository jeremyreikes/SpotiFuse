warnings.filterwarnings('ignore')
import spacy
nlp = spacy.load('en_core_web_sm')


def update_lyrics(subset = None):
    genius = lyricsgenius.Genius(genius_client_access_token)
    genius.remove_section_headers = True
    genius.verbose = False
    regex = re.compile('([\][])')
    if subset:
        cursor = tracks_db.find({'_id': {'$in': subset}, 'lyrics': {'$exists' : False}, 'name': {'$exists': True}, 'artist_name': {'$exists': True}})
    else:
        cursor = tracks_db.find({'lyrics': {'$exists' : False}, 'name': {'$exists': True}, 'artist_name': {'$exists': True}})
    for track in tqdm(cursor):
        tid = track['_id']
        track_name = track['name']
        artist_name = track['artist_name']
        try:
            song = genius.search_song(track_name, artist_name)
            lyrics = song.lyrics
            lyrics = lyrics.replace('\n', '. ')
            lyrics = re.sub(regex, '', lyrics)
            lyrics = lyrics.replace('. .', '.')
            tracks_db.find_one_and_update({'_id': tid}, {'$set': {'lyrics': lyrics}})
        except:
            tracks_db.find_one_and_update({'_id': tid}, {'$set': {'lyrics': None}})
