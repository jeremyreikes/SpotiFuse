import spacy
nlp = spacy.load('en_core_web_lg')
from pymongo import MongoClient
client = MongoClient(readPreference='secondary')
db = client.spotify_db
all_tracks = db.all_tracks
parsed_playlists = db.parsed_playlists
all_artists = db.all_artists


def lemmatize(doc):
    lemmas = list()
    for token in doc:
        if token.is_stop or not token.is_alpha:
            continue
        lemma = token.lemma_.strip().lower()
        if lemma and lemma != '-PRON-':
            lemmas.append(lemma)
    return set(lemmas)
