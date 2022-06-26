from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import sys, os
BASEPATH = os.path.split(__file__)[0]
sys.path.append(BASEPATH)

from gather import get_allwords, get_frequency
from workup import add_features,  add_predicted_avg

all_words = get_allwords()
df_freq = get_frequency()

app = FastAPI()

origins = [
    "http://coolsciencey.com",
    "https://coolsciencey.com",
    "http://www.coolsciencey.com",
    "https://www.coolsciencey.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/favicon.ico")
def get_favorico():
    return {'Hello':'World'}

@app.get('/wordleword/{wordleword}')
def predict_wordlescore(wordleword: str):
    wordleword = wordleword.upper()
    if len(wordleword)!=5:
        return {'Error': 'wordleword must be 5 characters'}
    df = pd.DataFrame({'wordleword':[wordleword]})
    in_all_words_list = False
    for word1 in all_words:
        if word1 == wordleword:
            in_all_words_list = True
    if not in_all_words_list:
        return {'Error': 'wordleword not in word list'}
    df = add_features(df, all_words, df_freq)
    df = add_predicted_avg(df)
    return df.iloc[0].to_json()#{'wordleword': df[0, 'wordleword'], 'avg_predicted': df.iloc[0,0]}
