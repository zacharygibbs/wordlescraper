"""
Various helper functions - 
Author - Zach Gibbs 6/8/2022

"""

from typing import Sequence, Union
import json, os, sys
import numpy as np
import pandas as pd
import ftplib

BASEPATH = os.path.split(__file__)[0]
sys.path.append(BASEPATH)

def get_avg(dfi: pd.DataFrame)->float:
    """
    function to compute the average wordle score
    note - assumes that pct_X counts as a numeric 7 guesses
    dfi - dataframe - single row (meant to be run through apply function)
    """
    cols = dfi.index
    return np.sum([np.float32(dfi.loc[col])/100 * (index + 1) for index,col in enumerate(cols)])

def get_stddev(dfi: pd.DataFrame(), avg: Union[float, None]=None)->float:
    """
    function to compute standard deviation
    note - assumes that pct_X counts as a numeric 7 guesses
    dfi - dataframe - single row (meant to be run through apply function)
    avg - default None
        if None, averages will be calculated
    """
    if avg==None:
        avg = get_avg(dfi)
    cols = dfi.index
    return np.sqrt(np.sum([np.float32(dfi.loc[col])/100 * (index + 1 - avg)**2 for index,col in enumerate(cols)]))

def get_skewness(dfi: pd.DataFrame, en: int, avg: float=None)->float:
    """
    method to calculate skewness
    dfi - dataframe - single row (meant to be run through apply function)
    en - int
        number of items in the distribution
    """
    if type(avg)==type(None):
        avg = get_avg(dfi)
    cols = dfi.index
    en = match_df_index(dfi, en)
    avg = match_df_index(dfi, avg)
    m3 = np.sum([np.float32(dfi.loc[col])/100 * (index + 1 - avg)**3 for index,col in enumerate(cols)])
    m2 = np.sum([np.float32(dfi.loc[col])/100 * (index + 1 - avg)**2 for index,col in enumerate(cols)])
    g1 = m3 / m2 ** 1.5
    gee1 = np.sqrt(en*(en-1)) / (en-2) * g1
    return gee1

def match_df_index(dfi, en):
    """
    helper method to keep df and i on same index
    """
    if type(en) == type(pd.DataFrame([])) or type(en)==type(pd.Series([])):
        en = en.loc[dfi.name]
        if type(en)==type(''):
            en = np.float32(en.replace(',',''))
    return en

def get_stats(df: pd.DataFrame, stat1: str, en=None):
    """
    function to apply statistics over an entire dataframe
    df - 
        DataFrame over which to apply statistics
    stat1 - str
        'avg', 'std', 'skewness' function to apply
    """
    pct_columns = df[[i for i in df.columns if 'pct_' in i]]
    funclist = {
        'avg':get_avg,
        'stddev':get_stddev,
        'skewness': lambda df1: get_skewness(df1, en=en)
    }
    return pct_columns.apply(funclist[stat1], axis=1)

def get_secret_json(from_file: str='secret_web.json')->dict:
    """
    load json from filename
    """
    try:
        with open(from_file, 'r') as f:
            sec = json.load(f)
    except:
        with open(os.path.join(BASEPATH, from_file), 'r') as f:
            sec = json.load(f)
    return sec

def send_ftp(
                host: str, 
                username: str, 
                password: str, 
                filenames: Sequence=("wordlestats_list.csv", "wordlestats_list.json"), 
                upload_path: str='public_html/wordle-stats-sciencey'
            )->None:
    """
    Based on example - https://www.geeksforgeeks.org/how-to-download-and-upload-files-in-ftp-server-using-python/
    sends a list of files via FTP to a web location
    """
    # Connect FTP Server
    ftp_server = ftplib.FTP(host, username, password)
    # force UTF-8 encoding
    ftp_server.encoding = "utf-8"
    # Enter File Name with Extension
    #filenames = ["wordlestats_list.csv", "wordlestats_list.json"]
    upload_path = 'public_html/wordle-stats-sciencey'
    # Read file in binary mode
    for filename in filenames:
        with open(filename, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR {os.path.join(upload_path,filename)}", file)
    # Get list of files
    ftp_server.dir(os.path.join(upload_path,filename))
    # Close the Connection
    ftp_server.quit()
