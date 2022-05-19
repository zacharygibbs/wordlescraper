#stats

import numpy as np
import scipy.stats
import pandas as pd
from functions_stats import get_avg, get_stddev, get_skewness

my_data = {
    'numresults': 83,
    'winpct': 98, 
    'pct_1': 0,
    'pct_2': 3,
    'pct_3': 19,
    'pct_4': 31,
    'pct_5': 21,
    'pct_6': 7
}
my_data = {# gina
    'numresults': 70,
    'winpct': 93, 
    'pct_1': 0,
    'pct_2': 2,
    'pct_3': 12,
    'pct_4': 19,
    'pct_5': 23,
    'pct_6': 9
}

my_data = pd.DataFrame(my_data, index=['my_data'])
total_wins = np.sum([my_data[i] for i in my_data if 'pct_' in i])
my_data['pct_X'] = my_data['numresults'] - total_wins
for col in my_data:
    if 'pct_' in col:
        my_data[col] = my_data[col] / total_wins * 100

pct_columns = my_data[[i for i in my_data.columns if 'pct_' in i]]
newcols = pct_columns.copy()
newcols['avg'] = pct_columns.apply(get_avg, axis=1)
newcols['stddev'] = pct_columns.apply(get_stddev, axis=1)
newcols['skewness'] = pct_columns.apply(get_skewness, axis=1, args=(my_data['numresults'], newcols['avg']))
my_data = my_data.drop(newcols.columns.tolist(), axis=1, errors='ignore')
my_data = pd.concat([my_data, newcols], axis=1)
my_data.to_csv('my_data_list.csv', index=False)