# wordlescraper

Initially intended to be a wordle web scraper - i'm now just using the Twitter API (and tweepy) and Google Sheets APIs (credit to [this sheet](https://docs.google.com/spreadsheets/d/1nl_kSpnsmY-qvez2OHvMmtIYfM7tZhP5embgmedMRxE/edit#gid=556946757) for keeping their sheet up to date)
to pull in Wordle Statistics and distribution data that are being aggregated by @wordlestats.

I have also pulled in a list of all possible [5 letter wordle words](https://github.com/tabatkins/wordle-list/blob/main/words)

Next step will be to attempt to make a link between the difficulty of the word (as measured by the Average # of guesses for that day). Also could check # of reports back - is it seasonal? is it growing or shrinking over time, is it more or fewer on the weekends? Also - it's possible if it's a hard day that fewer will tweet about it? look for some hypothesis testing

requires - 
tweepy
gspread

In order to run in automted fashion, you will need to update your crontab file with the path
to your conda distribution and the code itself in the crontab.txt file

once that is completed, you can add it to the linux automated cron jobs
```
crontab crontab.txt
crontab -l
```
which should add, then display the cron job
