#https://screenrant.com/wordle-answers-updated-word-puzzle-guide/
#https://docs.google.com/spreadsheets/d/1nl_kSpnsmY-qvez2OHvMmtIYfM7tZhP5embgmedMRxE/edit#gid=556946757

from ast import arg
import tweepy
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt

from functions_stats import get_avg, get_stddev, get_skewness

with open('secret.json','r') as f:
    secret = json.load(f)

def get_auth():
    auth = tweepy.OAuth2BearerHandler(secret['token'])
    api = tweepy.API(auth)
    return api

if __name__ == '__main__':
    api = get_auth()
    first_time = False
    num_tweets = 10 if not first_time else 1000 #assume this will run more often than every 10 days
    timeline = api.user_timeline(screen_name='wordlestats', count=num_tweets, tweet_mode='extended', exclude_replies=True)#user_id, screen_name, since_id, count, max_id, trim_user, exclude_replies, include_rts)
    if not first_time:
        tweet_list = pd.read_csv('tweet_list.csv')
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
    tweet_list.to_csv('tweet_list.csv', index=False)

