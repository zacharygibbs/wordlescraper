import pandas as pd
import gspread

#https://screenrant.com/wordle-answers-updated-word-puzzle-guide/
#https://docs.google.com/spreadsheets/d/1nl_kSpnsmY-qvez2OHvMmtIYfM7tZhP5embgmedMRxE/edit#gid=556946757

gc = gspread.service_account(filename='secret_g.json')
sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nl_kSpnsmY-qvez2OHvMmtIYfM7tZhP5embgmedMRxE/edit#gid=556946757')
values = sheet.values_get('A1:C1000')['values']

word_list = pd.DataFrame(values, columns = ['date', 'wordleid', 'wordleword'])
word_list['date'] = pd.to_datetime(word_list['date'])
word_list = word_list.sort_values('date')
word_list.to_csv('word_list.csv', index=False)