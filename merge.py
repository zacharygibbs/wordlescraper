import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions_stats import get_stats

tweet_list = pd.read_csv('tweet_list.csv')
word_list = pd.read_csv('word_list.csv')
all_words = pd.read_csv('allwords_list.csv',header=None)
tweet_list['numresults'] = tweet_list['numresults'].str.replace(',','').astype('float32')
tweet_list['avg'] = get_stats(tweet_list, 'avg')
tweet_list['stddev'] = get_stats(tweet_list, 'stddev')
tweet_list['skewness'] = get_stats(tweet_list, 'skewness', en=tweet_list['numresults'])
grand_avg = np.sum(tweet_list['avg'] * tweet_list['numresults']) / tweet_list['numresults'].sum()

my_data = False
if my_data:
    my_data =pd.read_csv('my_data_list.csv')
    print(f'grand avg:{grand_avg}, my_data: {my_data.avg}')
    

df = tweet_list.merge(word_list, how='left', on='wordleid')
df = df[['wordleid', 'date', 'wordleword', 'numresults', 'pct_1', 'pct_2', 'pct_3', 'pct_4', 'pct_5', 'pct_6', 'pct_X', 'avg', 'stddev']]

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date', ascending=False)

df.to_csv('wordlestats_list.csv')




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