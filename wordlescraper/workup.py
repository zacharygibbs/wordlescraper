import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

from helpers import get_stats
from workup import gather_all


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

def get_number_of_matching_all(word_to_check, df_allwords):
    a = df_allwords.iloc[:,0]
    matching = pd.DataFrame({'matches':[0]*len(a)})
    for letter in word_to_check:
        matching['matches'] = matching['matches'] + a.str.count(letter)
    result = matching['matches']\
                .value_counts()\
                .reset_index()\
                .sort_values('index')
    return dict(zip(result['index'], result['matches']))

def merge_num_matches(df, df_allwords):
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

def duplicate_letters(wordleword):
    count = 0
    for letter in wordleword:
        if wordleword.count(letter) > 1:
            count += 0.5
    return count

def merge_duplicate_letters(df):
    df['duplicate_letters'] = df['wordleword'].apply(duplicate_letters)
    return df

def get_scrabble_score(wordleword):
    letter_score = {
        'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4,
        'G':2, 'H':4, 'I':1, 'J':8, 'K':5, 'L':1,
        'M':3, 'N':1, 'O':1, 'P':3, 'Q':10, 'R':1,
        'S':1, 'T':1, 'U':1, 'V':4, 'W':4, 'X':8,
        'Y':4, 'Z':10
    }
    score = 0
    for letter in wordleword:
        score += letter_score[letter]
    return score

def merge_scrabble_score(df):
    df['scrabblescore'] = df['wordleword'].apply(get_scrabble_score)
    return df

def merge_starts_with_vowel(df):
    df['starts_with_vowel'] = [int(i[0] in ('A','E','I','O', 'U')) for i in df['wordleword']]
    return df

def merge_num_vowels(df):
    df['num_vowels'] = [np.sum([int(j in ('A','E','I','O', 'U')) for j in i]) for i in df['wordleword']]
    return df

def merge_coarse_grain(df):
    df['pctCG_good'] = df['pct_1'] + df['pct_2'] + df['pct_3']
    df['pctCG_medium'] = df['pct_4']
    df['pctCG_bad'] = df['pct_5'] + df['pct_6'] + df['pct_X']
    return df

if __name__ == '__main__':
    all_words, word_list, tweet_list, df_freq = gather_all()
    df = merge_gathered(tweet_list=tweet_list, word_list=word_list)
    df = merge_freq(df=df, df_freq=df_freq)


#Work up all words - letter frequency table, words with duplicate letters, other items below?
# compare 'all words' with the ones played so far


### Some things that could be done?

#Step 1 - 
#Enter in your wordle score distribution and find out how you compare to the average. 
#Create simple javascript app to house this

# Step 2 - statistics
# metrics - Average; Skewness; # of people who do not get it

# things to check against

#Vowel frequency (which vowels show up more often)
#Vowel number of (how many vowels are in final answer) - see if this affects how many people get it?
#Vowel in which position (1st last etc). 
#Has repeated letters 
#Starts with vowel?
#Has U or Y?  or other 'uncommon' letters - common as given by letter frequency #uncommon consonants vs vowels
#Consonants frequency, consonant positons
##### check for strange letters; letter frequency in full word set



perform_workup = False

if perform_workup:
    fig1, ax1 = plt.subplots(1, 1)
    ax1.plot(df['date'], df['avg'], 'bo')
    ax1.plot(df['date'], np.ones(len(df))* df['avg'].mean(), 'k--')
    ax1.set_ylabel('Avg Number of Guesses')
    plt.show()
