import pandas as pd
import re
import os

from bs4 import BeautifulSoup
import urllib.request
url = "http://screenrant.com/wordle-answers-updated-word-puzzle-guide/"
sock = urllib.request.urlopen(url).read().decode("utf-8")

soup = BeautifulSoup(sock, 'html.parser')
#print(soup.prettify())

if os.path.exists('word_list.csv'):
    word_list_old = pd.read_csv('word_list.csv')
else:
    word_list_old = None

tag = soup.find_all("li", recursive=True)
tag = pd.Series(tag)
tag = tag.astype(str)
word_list = tag.str.extract(r"(?P<date>[A-Z][a-z]*\D*\d{2}) - #(?P<wordleid>\d{2,5})[^A-Z]*(?P<wordleword>[A-Z]*)")\
               .dropna()
word_list['wordleid'] = word_list["wordleid"].astype("int64")
if word_list_old:
    word_list = pd.concat([word_list, word_list_old]).drop_duplicates()
else:
    word_list = word_list.drop_duplicates()
word_list.to_csv('word_list.csv', index=False)

#shard, pleat, aloft, skill, frame ,caulk; all of the Jan ones

#list(zip(range(len(tag)), tagnew["Word"], tag))


#todays-wordle-hints-answer-march-30th-284/"><strong>Mar 30 - #284</strong> - STOVE</a></li>,
# <li><a href="https://screenrant.com/what-is-todays-wordle-hints-answer-march-31st-285/"><strong>Mar 31 - #285</strong> - LOWLY</a></li>,
# <li><a href="https://screenrant.com/wordle-227-february-1-answer-hints-solution-guide/"><strong>Feb 01 - #227</strong> - THOSE</a></li>,
# <li><a href="https://screenrant.com/wordle-228-february-2-2022-answer/"><strong>Feb 02 - #228</strong> - MOIST</a></li>,
# <li><a href="https://screenrant.com/wordle-229-february-3-2022-answer/"><strong>Feb 03 - #229</strong> - SHARD</a></li>,
# <li><a href="https://screenrant.com/wordle-230-february-4-answer-hints-solution-guide/"><strong>Feb 04 - #230</strong> - PLEAT</a></

#https://screenrant.com/wordle-answers-updated-word-puzzle-guide/
#https://docs.google.com/spreadsheets/d/1nl_kSpnsmY-qvez2OHvMmtIYfM7tZhP5embgmedMRxE/edit#gid=556946757

#gc = gspread.service_account(filename='secret_g.json')
#sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nl_kSpnsmY-qvez2OHvMmtIYfM7tZhP5embgmedMRxE/edit#gid=556946757')
#values = sheet.values_get('A1:C1000')['values']

#word_list = pd.DataFrame(values, columns = ['date', 'wordleid', 'wordleword'])
#word_list['date'] = pd.to_datetime(word_list['date'])
#word_list = word_list.sort_values('date')
#word_list.to_csv('word_list.csv', index=False)


