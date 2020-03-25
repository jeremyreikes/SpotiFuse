import twint
import nest_asyncio
nest_asyncio.apply()
import pandas as pd
import pickle
from tqdm import tqdm
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
import time

# get spotify shares based on link instead -
def get_tweets(track):
    track_name = track.track_name
    artist = track.artist
    c = twint.Config()
    c.Pandas = True
    c.Pandas_clean = True
    c.Hide_output = True
    c.Limit=1000
    c.Search = track_name
    twint.run.Search(c)
    df = twint.storage.panda.Tweets_df
    if df.empty:
        return ''
    tweets_str = ' '.join(list(df.tweet))
    return tweets_str

def get_tweet_word_counts(tracks):
    tweet_word_counts = defaultdict(Counter)
    ps = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    for index, track in tqdm(tracks.iterrows()):
        tweets = get_tweets(track)
        words = tokenizer.tokenize(tweets)
        for word in words:
            stemmed_word = ps.stem(word.lower())
            tweet_word_counts[track.tid][stemmed_word] += 1
    return tweet_word_counts

tracks = pd.read_csv('tids_100000-200000.csv')
word_counts = get_tweet_word_counts(tracks.iloc[:1000])
tracks.tail(100)
tracks.head()
tweets = get_tweets(tracks.loc[99909])
len(tweets)
