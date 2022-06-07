# wordlescraper / wordle-stats-sciencey - Zach Gibbs 2022
A python-based data gathering and statistics application that gathers daily wordle statistics ([@wordlestats](https://twitter.com/wordlestats)) and links merges those with the [daily winning word](https://screenrant.com/wordle-answers-updated-word-puzzle-guide/). (wordlescraper/)

A front end application is attached, written in Javascript/Svelte/Sveltekit that displays the daily results and allows users to enter in their own wordle results (wordle_stats_frontend/)

Additionally, data analytics/machine learning is performed using the gathered dataset to help determine what factors are most important when it comes to the average number of guesses for a given word. (WordleStatsAnalytics.ipynb)

# Getting Started

## Python 
### Installation
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

### Credentials Setup

### Python Running Nightly Data Pull - Cron Job
In order to run in automted fashion, you will need to update your crontab file with the path
to your conda distribution and the code itself in the crontab.txt file

once that is completed, you can add it to the linux automated cron jobs
```
crontab crontab.txt
crontab -l
```
which should add, then display the cron job

### Python Running Jupyter Analytics Notebook  

## Javascript

### Install Sveltekit
node.js:
    see package.json file

### pnpm run dev


# References
1) ([@wordlestats](https://twitter.com/wordlestats)) Twitter Bot
2) [daily winning word](https://screenrant.com/wordle-answers-updated-word-puzzle-guide/) Screenrant.com
3) all possible wordle answers: [csokolove/wordle-word-list](https://github.com/csokolove/wordle-word-list)
4) 'frequency' list of 300,000 english words [kaggle: rtatman/english-word-frequency](https://www.kaggle.com/datasets/rtatman/english-word-frequency)