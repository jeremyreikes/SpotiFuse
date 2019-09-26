from pymongo import MongoClient
client = MongoClient(readPreference='secondary')
all_artists = client.spotify_db.all_artists
from pandas.io.json import json_normalize
import warnings
warnings.filterwarnings('ignore')
import pandas as pd

import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt
%matplotlib inline
pyLDAvis.enable_notebook()
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel
genre_model = LdaModel.load('lda_models/genre.model')
subgenre_model = LdaModel.load('lda_models/subgenre.model')


def get_all_genres():
    datapoints = list(all_artists.find({}, {'genres': 1}))
    df = json_normalize(datapoints)
    df.set_index('_id', inplace=True)
    df = df[df['genres'].map(lambda x: type(x) != float)]
    df = df[df['genres'].map(lambda x: len(x)) > 0]
    return df


def create_models(df):
    ''' creates/saves two LDA models (one genre, one subgenre) in a folder called lda_models '''
    df = get_all_genres()
    id2word = corpora.Dictionary(df.genres)
    word2id = {v: k for k, v in id2word.items()}
    corpus = [id2word.doc2bow(genres) for genres in df.genres]
    # captures subgenres with 50 categories
    subgenre_model = LdaModel(corpus=corpus,
                              id2word=id2word,
                              num_topics=50,
                              random_state=100,
                              update_every=1,
                              passes=5,
                              alpha='auto',
                              per_word_topics=True)
    # capture main genres with 10 categories
    genre_model = LdaModel(corpus=corpus,
                           id2word=id2word,
                           num_topics=10,
                           random_state=100,
                           update_every=1,
                           passes=5,
                           alpha='auto',
                           per_word_topics=True)
    subgenre_model.save('lda_models/subgenre.model')
    genre_model.save('lda_models/genre.model')


def load_models():
    genre_model = LdaModel.load('lda_models/genre.model')
    subgenre_model = LdaModel.load('lda_models/subgenre.model')
    return genre_model, subgenre_model

def get_genre_preds(list_of_genres):
    # genre_model, subgenre_model = load_models()
    all_genre_preds = list()
    all_subgenre_preds = list()
    subgenre_id2word = subgenre_model.id2word
    genre_id2word = genre_model.id2word
    for genres in list_of_genres:
        subgenre_preds = subgenre_model[subgenre_id2word.doc2bow(genres)]
        all_subgenre_preds.append(subgenre_preds[0])
        genre_preds = genre_model[genre_id2word.doc2bow(genres)]
        all_genre_preds.append(genre_preds[0])
    return all_genre_preds, all_subgenre_preds

def plot_topics(model, corpus, id2word):
    return pyLDAvis.gensim.prepare(model, corpus, id2word)


#
def add_genre_preds(all_genre_preds, subgenre_preds):
