# wordlescraper / wordle-stats-sciencey - Zach Gibbs 2022
A python-based data gathering and statistics application that gathers daily wordle statistics ([@wordlestats](https://twitter.com/wordlestats)) and links merges those with the [daily winning word](https://screenrant.com/wordle-answers-updated-word-puzzle-guide/). (wordlescraper/)

A front end application is attached, written in Javascript/Svelte/Sveltekit that displays the daily results and allows users to enter in their own wordle results (wordle_stats_frontend/)

Additionally, data analytics/machine learning is performed using the gathered dataset to help determine what factors are most important when it comes to the average number of guesses for a given word. (WordleStatsAnalytics.ipynb)

# Getting Started

## Python 
### Installation
A [conda environment](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links) can be built by running the following command in the shell
```
cd wordlescraper
conda env create -f conda_wordlestats.yml
conda activate wordlestats
```

### Credentials Setup
credentials should be set up using 'secret_*.json' files located in the 'wordlescraper/wordlescraper/' folder.
secret.json
    Should contain a json dictionary with key 'token' with an active [Twitter API key](https://developer.twitter.com/en/docs/twitter-api)
```
{"token":"ABCDEFGTWITTERAPIKEYHERE"}
```
secret_web.json
    should contain FTP credentials
```
{"host": "ftphosthere.com", "username": "your_username","password": "your_password_321"}
```

Optionally - if you would like to access the [kaggle word frequency dataset](https://www.kaggle.com/datasets/rtatman/english-word-frequency) in order to run the anaytics workbook, it can be downloaded from here (or with the kaggle api)
once set up with a ~/.kaggle/kaggle.json username and key, run the shell script:
```
cd wordlestats
bash get_kaggle_frequency_dataset.sh
```

### Python Running Nightly Data Pull - Cron Job
In order to run in automated fashion, you will need to update your crontab file with the path
to your conda distribution and the code itself in the crontab.txt file. 

You will also want to update the get_all.sh script with the correct wordlescraper/wordlescraper directory

once that is completed, you can add it to the linux automated cron jobs
```
crontab crontab.txt
crontab -l
```
which should add, then display the cron job

## Javascript
node.js - build using:

```
cd wordle_stats_frontend
npm install
```
or optionaly
```
pnpm install
```

# References
1) ([@wordlestats](https://twitter.com/wordlestats)) Twitter Bot
2) [daily winning word](https://screenrant.com/wordle-answers-updated-word-puzzle-guide/) Screenrant.com
3) all possible wordle answers: [csokolove/wordle-word-list](https://github.com/csokolove/wordle-word-list)
4) 'frequency' list of 300,000 english words [kaggle: rtatman/english-word-frequency](https://www.kaggle.com/datasets/rtatman/english-word-frequency)