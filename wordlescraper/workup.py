"""
This file contains various functions for performing data workup tasks including
merging data from various sources and adding features for datascience workup
Author - Zach Gibbs 6/8/2022
"""

from typing import Callable

import joblib
import pandas as pd
import numpy as np
import sys, os
BASEPATH = os.path.split(__file__)[0]
sys.path.append(BASEPATH)


from helpers import get_stats, send_ftp, get_secret_json
from gather import gather_all

SCRABBLE_LETTER_SCORE = {
    'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4,
    'G':2, 'H':4, 'I':1, 'J':8, 'K':5, 'L':1,
    'M':3, 'N':1, 'O':1, 'P':3, 'Q':10, 'R':1,
    'S':1, 'T':1, 'U':1, 'V':4, 'W':4, 'X':8,
    'Y':4, 'Z':10
}

VOWELS = ('A','E','I','O', 'U')

def merge_gathered(tweet_list: pd.DataFrame, word_list: pd.DataFrame) -> pd.DataFrame:
    """ 
    function to merge tweet_list results with word_list (correct answers)
    tweet_list - pd.DataFrame
        DataFrame output from gather.get_tweets
    word_list - pd.DataFrame
        dataframe output from gather.get_wordlist
    returns
        merged dataframe with statistics (avg, std) pct_ score distribution, and wordleword
    """
    tweet_list['numresults'] = tweet_list['numresults'].str.replace(',','').astype('float32')
    tweet_list['avg'] = get_stats(tweet_list, 'avg')
    tweet_list['stddev'] = get_stats(tweet_list, 'stddev')
    tweet_list['skewness'] = get_stats(tweet_list, 'skewness', en=tweet_list['numresults'])
    grand_avg = np.sum(tweet_list['avg'] * tweet_list['numresults']) / tweet_list['numresults'].sum()
    tweet_list = tweet_list.copy().dropna(how="any")
    tweet_list['date'] = pd.to_datetime( tweet_list.copy()[['year', 'month', 'day']])
    tweet_list['wordleid'] = tweet_list.copy()['wordleid'].astype('int64')
    df = tweet_list.merge(word_list.drop('date',axis=1), how='left', on='wordleid')
    df = df[['wordleid', 'date', 'wordleword', 'numresults', 'pct_1', 'pct_2', 'pct_3', 'pct_4', 'pct_5', 'pct_6', 'pct_X', 'avg', 'stddev']]
    df = df.sort_values('date', ascending=False)
    df = df.reset_index()
    df.to_csv('wordlestats_list.csv')
    df.to_json('wordlestats_list.json')
    return df

def merge_freq(df: pd.DataFrame, df_freq: pd.DataFrame) -> pd.DataFrame:
    """
    function to add frequency features to dataset
    df - DataFrame
        DataFrame of tweet scores to be merged on wordleword
    df_freq - DataFrame
        DataFrame containing wordlewords and their respective frequency
    returns
        modified dataframe with 'freq' and 'logfreq' features added
    """
    df = df.merge(df_freq, how='left', on='wordleword').drop_duplicates()
    df['logfreq'] = np.log10(df['freq'])
    return df

def get_number_of_matching_all(word_to_check: str, df_allwords: pd.DataFrame)->dict:
    """ 
    checks word_to_check to determine how many words in df_allwords match 1, 2, 3, 4, or 5 letters
    can be used as a metric of a words similarity to other words in the wordle possible word list
    word_to_check - str
        inputted word to check
    df_allwords - pd.DataFrame 
        list of all wordle words (words must be in first column of DataFrame or Series)
    """
    allwords = df_allwords#.iloc[:,0].str.upper()
    matching = pd.DataFrame({'matches':[0]*len(allwords)})
    for letter in word_to_check:
        matching['matches'] = matching['matches'] + allwords.str.count(letter)
    result = matching['matches']\
                .value_counts()\
                .reset_index()\
                .sort_values('index')
    return dict(zip(result['index'], result['matches']))

def merge_num_matches(df: pd.DataFrame, df_allwords: pd.DataFrame)->pd.DataFrame:
    """
    function to synthesize the number of letter matches (get_number_of_matching_all) and execute
    for all words in df, then merge the results with df
    df - pd.DataFrame
        input dataframe (with wordleword column at minimum) to determine matches for
    df_allwords - pd.DataFrame
        word list of df to count matching letters against (i.e. all possible wordle words)
    """
    num_matches = pd.DataFrame({'wordleword': [], 'letter_matches_2':[], 'letter_matches_3':[], 'letter_matches_4':[], 'letter_matches_5':[]})
    for wordleword in df['wordleword'].values:
        matches = get_number_of_matching_all(wordleword, df_allwords)
        num_matches = pd.concat([
            num_matches, 
            pd.DataFrame({
                'wordleword': [wordleword],
                'letter_matches_2':[matches.get(2, 0)], 
                'letter_matches_3':[matches.get(3, 0)], 
                'letter_matches_4':[matches.get(4, 0)], 
                'letter_matches_5':[matches.get(5, 0)]
            })
        ], axis=0, ignore_index=True)
    df = df.merge(num_matches, how='left', on='wordleword')
    return df

def duplicate_letters(wordleword: str)->int:
    """
    function to determine number of duplicate letters in a string
    wordleword - str
        word to check for duplicates
    """
    count = 0
    for letter in wordleword:
        if wordleword.count(letter) > 1:
            count += 1
    return count/2

def get_scrabble_score(wordleword: str)->int:
    """
    function to determine a words scrabble score
    wordleword - str
        input word to determine score
    returns
        score as integer
    """
    score = 0
    for letter in wordleword:
        score += SCRABBLE_LETTER_SCORE[letter]
    return score

def starts_with_vowel(wordleword):
    "returns 1 if starts with vowel, 0 otherwise"
    return int(wordleword[0] in VOWELS)

def num_vowels(wordleword):
    "returns number of vowels in the word"
    return np.sum([int(j in VOWELS) for j in wordleword])

def merge_generic(df: pd.DataFrame, func: Callable, colname: str)-> pd.DataFrame:
    """
    generic function to apply a function over the wordleword column
    df - pd.DataFrame
        DataFrame that should have 'wordleword' column that func should be applied to
    func - function
        function that works on a single wordleword
    colname - str
        the resulting string
    returns
        dfnew - result of applying function and creating new column - colname
    """
    dfnew = df.copy()
    dfnew[colname] = dfnew['wordleword'].apply(func)
    return dfnew

def merge_coarse_grain(df: pd.DataFrame)->pd.DataFrame:
    """
    function to add some y-variables that aggregate percentages into good, medium, and bad categories
    where 1,2,3 guesses = good; 4 = medium; and 5, 6, X = bad
    returns
        df with columns added - pctCG_good pct_CG_medium pctCG_bad
    """
    for col in [i for i in df.columns if 'pct_' in i]:
        df[col] = df[col].astype(float)
    df['pctCG_good'] = df['pct_1'] + df['pct_2'] + df['pct_3']
    df['pctCG_medium'] = df['pct_4']
    df['pctCG_bad'] = df['pct_5'] + df['pct_6'] + df['pct_X']
    return df

def add_features(
    df: pd.DataFrame,
    all_words: pd.DataFrame, 
    df_freq: pd.DataFrame
    )-> pd.DataFrame:
    """
    function to execute all workup / merge steps to add features
    df - pd.DataFrame
        inputted df - must have wordleword column; usually from merged tweets/word_list
    all_words - pd.DataFrame
        entire list of possible wordlewords - pd.Series or DataFrame with list in first column
    df_freq - pd.DataFrame
        list of 300,000 english words - see gather.get_frequency function
    returns
        pd.DataFrame with features added
    """
    df = merge_freq(df=df, df_freq=df_freq)
    df = merge_num_matches(df, df_allwords=all_words)
    df = merge_generic(df, duplicate_letters, 'duplicate_letters')
    df = merge_generic(df, get_scrabble_score, 'scrabblescore')
    df = merge_generic(df, num_vowels, 'num_vowels')
    df = merge_generic(df, starts_with_vowel, 'starts_with_vowel')
    return df

def gather_and_workup(to_file_csv: str='wordlestats_list.csv', to_file_json: str='wordlestats_list.json', first_time: bool=False):
    """
    Run all gather and workup scripts and write to file
    """
    all_words, word_list, tweet_list, df_freq = gather_all(first_time=first_time)
    df = merge_gathered(tweet_list=tweet_list, word_list=word_list)
    df = df.dropna(how='any', axis=0)
    df = add_features(df, all_words=all_words, df_freq=df_freq)
    df = merge_coarse_grain(df)
    df = add_predicted_avg(df)
    df.to_csv(to_file_csv)
    df.to_json(to_file_json)
    return df

def add_predicted_avg(df: pd.DataFrame)->pd.DataFrame:
    """
    add ridge regression model prediction for average
    """
    bp = '' if os.path.exists('scl_x.pickle') else BASEPATH
    scl_x = joblib.load(os.path.join(bp, 'scl_x.pickle'))
    scl_y = joblib.load(os.path.join(bp, 'scl_y.pickle'))
    model = joblib.load(os.path.join(bp, 'ridge_model.pickle'))
    df_trial = df.copy()#[['wordleword', 'logfreq', 'duplicate_letters', 'scrabblescore']]
    X_trial = df_trial[['logfreq', 'duplicate_letters', 'scrabblescore']]
    X_scl_trial = scl_x.transform(X_trial)
    df_trial['avg_predicted'] = scl_y.inverse_transform(model.predict(X_scl_trial)).transpose()[0,:]
    return df_trial

if __name__ == '__main__':
    df = gather_and_workup(first_time=False)
    secret = get_secret_json('secret_web.json')
    send_ftp(secret['host'], secret['username'], secret['password'])
    #all_words, word_list, tweet_list, df_freq = gather_all(first_time=False)
    #df = merge_gathered(tweet_list=tweet_list, word_list=word_list)
    #df = df.dropna(how='any', axis=0)
    #df = add_features(df, all_words=all_words, df_freq=df_freq)
    #df = merge_coarse_grain(df)

