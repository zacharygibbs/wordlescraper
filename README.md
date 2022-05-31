# wordlescraper
## A web application that scrapes for wordle statistics and correct answers, then displays such on a website
## Also, data analytics to estimate model

Initially intended to be a wordle web scraper - i'm now just using the Twitter API (and tweepy) to pull in Wordle Statistics and distribution data that are being aggregated by [@wordlestats](https://twitter.com/wordlestats) twitter bot.

I am also scraping for correct answers on [screenrant.com](https://screenrant.com/wordle-answers-updated-word-puzzle-guide/).

I also pulled together information relating to all possible wordle answers: [csokolove/wordle-word-list](https://github.com/csokolove/wordle-word-list); along with a 'frequency' list of 300,000 english words [kaggle: rtatman/english-word-frequency](https://www.kaggle.com/datasets/rtatman/english-word-frequency).

requires - 
Python:
    tweepy
    beautifulsoup4
    pandas
    numpy
    scipy
    matplotlib
    seaborn
    statsmodels
    scikit-learn

node.js:
    see package.json file


# Instructions to run nightly data pull

In order to run in automted fashion, you will need to update your crontab file with the path
to your conda distribution and the code itself in the crontab.txt file

once that is completed, you can add it to the linux automated cron jobs
```
crontab crontab.txt
crontab -l
```
which should add, then display the cron job
