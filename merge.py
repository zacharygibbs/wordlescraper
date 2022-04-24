import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tweet_list = pd.read_csv('tweet_list.csv')
word_list = pd.read_csv('word_list.csv')

df = tweet_list.merge(word_list, how='left', on='wordleid')
df = df[['wordleid', 'date', 'wordleword', 'numresults', 'pct_1', 'pct_2', 'pct_3', 'pct_4', 'pct_5', 'pct_6', 'pct_X', 'avg', 'stddev']]

df['date'] = pd.to_datetime(df['date'])

all_words = pd.read_table('https://raw.githubusercontent.com/tabatkins/wordle-list/main/words')

### Some things that could be done?

#check for strange letters; letter frequency in full word set
#

perform_workup = False

if perform_workup:
    fig1, ax1 = plt.subplots(1, 1)
    ax1.plot(df['date'], df['avg'], 'bo')
    ax1.plot(df['date'], np.ones(len(df))* df['avg'].mean(), 'k--')
    ax1.set_ylabel('Avg Number of Guesses')
    plt.show()