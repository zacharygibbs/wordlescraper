import pandas as pd

all_words = pd.read_table('https://raw.githubusercontent.com/csokolove/wordle-word-list/main/wordlist.csv', header=None)#'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words', header=None)
all_words.to_csv('allwords_list.csv', index=False)