"""
This file is meant to gather wordle specific data from various sources
Author - Zach Gibbs 6/8/2022
"""

import os
import json
from telnetlib import SE
from typing import Sequence
import pandas as pd
import tweepy
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

from helpers import get_secret_json

def gather_all(first_time: bool) -> Sequence[pd.DataFrame]:
    """
    function meant to pull from all data sources, write to csvs, and return dataframes
    first_time - bool
        whether or not you have to pull all tweets or just 10
    returns 
        Tuple(all_words, word_list, tweet_list, df_freq)
    """
    all_words = get_allwords()
    word_list = get_wordlist()
    tweet_api = get_tweet_auth()
    tweet_list = get_tweets(tweet_api, first_time=first_time)
    df_freq = get_frequency()
    return (all_words, word_list, tweet_list, df_freq)

def get_allwords(to_file: str='allwords_list.csv') -> pd.DataFrame:
    """ 
    function to download all wordle possible words and write to csv
    returns
        all_words pandas DataFrame containing all possible wordle words
    """
    all_words = pd.read_table(
        'https://raw.githubusercontent.com/csokolove/wordle-word-list/main/wordlist.csv',
        header=None
    )
    all_words = all_words.iloc[:,0].str.upper()
    all_words.to_csv(to_file, index=False)
    return all_words
    
def get_tweets(api: tweepy.API, first_time: bool=True, to_file: str='tweet_list.csv') -> pd.DataFrame:
    """
    function to download wordlestats tweets
    api - instantiate with 'get_tweet_auth' function using secret.json file
    first_time - bool - default True - 
        if False, reads old file and adds last 10 days, if True ignores old file, reads 1000 tweets
    to_file - str - default 'tweet_list.csv'
        file to be written
    returns
        tweet_list pandas DataFrame containing full list of tweets
    """
    num_tweets = 10 if not first_time else 1000 #assume this will run more often than every 10 days
    timeline = api.user_timeline(screen_name='wordlestats', count=num_tweets, tweet_mode='extended', exclude_replies=True)#user_id, screen_name, since_id, count, max_id, trim_user, exclude_replies, include_rts)
    if not first_time:
        tweet_list = pd.read_csv(to_file)
        tweet_list['id_str'] = tweet_list['id_str'].astype(str)
    else:
        tweet_list = pd.DataFrame({'id_str':[]})
    for tweet in timeline:
        if not (tweet.id_str in tweet_list['id_str'].tolist()):
            df = pd.DataFrame({
                'id_str': [tweet.id_str],
                'created_at': [tweet.created_at],
                'full_text': [tweet.full_text]
            })
            df['created_at'] = pd.to_datetime(df['created_at'])
            tweet_list = pd.concat([tweet_list, df], ignore_index=True)
            print(f'added tweet id {tweet.id_str}: from {tweet.created_at}')
    #tweet_list['created_at'] = pd.to_datetime(tweet_list['created_at'])
    newcols = tweet_list['full_text'].str.extract(r'Wordle\s*(?P<wordleid>\d{,5}) (?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\n(?P<numresults>[\d,]*).*\n(?P<numhardmode>[\d,]*).*\n{,2}1:\D*(?P<pct_1>\d+)%\n2:\D*(?P<pct_2>\d+)%\n3:\D*(?P<pct_3>\d+)%\n4:\D*(?P<pct_4>\d+)%\n5:\D*(?P<pct_5>\d+)%\n6:\D*(?P<pct_6>\d+)%\nX:\D*(?P<pct_X>\d+)%\n')
    if not first_time:    
        tweet_list = tweet_list.drop(newcols.columns.tolist(), axis=1, errors='ignore')
    tweet_list = pd.concat([tweet_list, newcols], axis=1)
    tweet_list.to_csv(to_file, index=False)
    return tweet_list


def get_tweet_auth(auth_secret: str='secret.json') -> tweepy.API:
    """
    get 'token' from secret.json file, create Twitter API connection
    auth_secret
        should be a json filename that has a 'token' key
    """
    secret = get_secret_json(auth_secret)
    auth = tweepy.OAuth2BearerHandler(secret['token'])
    api = tweepy.API(auth)
    return api

def get_wordlist(to_file: str='word_list.csv') -> pd.DataFrame:
    """
    function to scrape history of correct wordle results
    to_file - str - default 'word_list.csv'
        file to be written
    returns
        word_list pandas DataFrame containing correct wordle answers
    """
    url = "http://screenrant.com/wordle-answers-updated-word-puzzle-guide/"
    sock = urllib.request.urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(sock, 'html.parser')
    #print(soup.prettify())
    if os.path.exists(to_file):
        word_list_old = pd.read_csv(to_file)
    else:
        word_list_old = ()
    tag = soup.find_all("li", recursive=True)
    tag = pd.Series(tag)
    tag = tag.astype(str)
    word_list = tag.str.extract(r"(?P<date>[A-Z][a-z]*\D*\d{2}) - #(?P<wordleid>\d{2,5})[^A-Z]*(?P<wordleword>[A-Z]*)")\
                .dropna()
    word_list['wordleid'] = word_list["wordleid"].astype("int64")
    if len(word_list_old)>0:
        word_list = pd.concat([word_list, word_list_old]).drop_duplicates()
    else:
        word_list = word_list.drop_duplicates()
    word_list.to_csv(to_file, index=False)
    return word_list

def get_frequency(from_kaggle: bool=False, to_file: str='unigram_freq.csv') -> pd.DataFrame:
    """ 
    function to both download english word frequency dataset from kaggle (https://www.kaggle.com/datasets/rtatman/english-word-frequency)
    and to load the csv into python
    from_kaggle - bool - default False
        if True will run script to download kaggle data (kaggle API must be installed and configured)
    to_file - str - default 'unigram_freq.csv'
        string for filename to load containing frequency dataset
    returns
        df_freq - frequency dataset
    """
    if from_kaggle:
        os.system('sh get_kaggle_frequency_dataset.sh')
    df_freq = pd.read_csv(to_file)
    df_freq['word'] = df_freq['word'].str.upper()
    df_freq = df_freq.rename(columns={'word':'wordleword', 'count':'freq'})
    return df_freq

if __name__=='__main__':
    all_words, word_list, tweet_list, df_freq = gather_all()

