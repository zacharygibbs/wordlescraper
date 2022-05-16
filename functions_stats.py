import numpy as np
import pandas as pd

def get_avg(dfi):
    #how to count those who did not get it? make them count as a 7? or instead get the average of only the people who did
    #cols = [i for i in dfi.index if '_X' not in i]
    cols = dfi.index
    return np.sum([np.float32(dfi.loc[col])/100 * (index + 1) for index,col in enumerate(cols)])

def get_stddev(dfi, avg=None):
    #how to count those who did not get it? make them count as a 7? or instead get the average of only the people who did
    #cols = [i for i in dfi.index if '_X' not in i]
    # sqrt( sum( (x-xbar)^2 / N) )
    # sqrt( sum(p_i * Number Total * (i - xbar)**2 / Number Total)) = sqrt( sum( p_1 * (i - xbar)**2))
    if avg==None:
        avg = get_avg(dfi)
    cols = dfi.index
    return np.sqrt(np.sum([np.float32(dfi.loc[col])/100 * (index + 1 - avg)**2 for index,col in enumerate(cols)]))

def get_skewness(dfi, en, avg=None):
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
    if type(en) == type(pd.DataFrame([])) or type(en)==type(pd.Series([])):
        en = en.loc[dfi.name]
        if type(en)==type(''):
            en = np.float32(en.replace(',',''))
    return en

def get_stats(df, stat1, en=None):
    pct_columns = df[[i for i in df.columns if 'pct_' in i]]
    funclist = {
        'avg':get_avg,
        'stddev':get_stddev,
        'skewness': lambda df1: get_skewness(df1, en=en)
    }
    return pct_columns.apply(funclist[stat1], axis=1)

