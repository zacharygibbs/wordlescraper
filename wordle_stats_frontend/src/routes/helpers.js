import * as d3 from 'd3';
import { 
    df,
    isMounted,
} from '../../stores.js'


export const KEYLISTDEFAULTY = ['avg', 'stddev', 'pctCG_good', 'pctCG_medium', 'pctCG_bad'];
export const EXCLUDEKEY = ['wordleid', 'wordleword', 'date', 'index'];
export const KEYLISTDEFAULTX = ['wordleid', 'logfreq', 'scrabblescore', 'duplicate_letters', 'letter_matches_2', 'letter_matches_3', 'letter_matches_4', 'letter_matches_5', 'num_vowels', 'starts_with_vowel', 'freq'];
export const EXCLUDEKEYX = ['date', 'index', 'avg', 'stddev', 'pctCG_good', 'pctCG_medium', 'pctCG_bad', 'pct_1', 'pct_2', 'pct_3', 'pct_4', 'pct_5', 'pct_6', 'pct_X'];
export const CHARTMODE = 'markers';
export const dotprod = (df, var1, var2) => {
    return df[var1].reduce(
        (total, curval, curind) => {
            return total + df[var1][curind]*df[var2][curind]
        }, 0
    )
}

export const sum = (arr) => {
    return arr.reduce(function (a, b) {
        return a + b;
    }, 0);
}

export const setSelectedValue = (selectObj, valueToSet) => {
    for (var i = 0; i < selectObj.options.length; i++) {
        if (selectObj.options[i].text== valueToSet) {
            selectObj.options[i].selected = true;
            return;
        }
    }
}

export const calcAvg = (pct1, pct2, pct3, pct4, pct5, pct6, pctx) => {
    return (pct1 * 1 + pct2 * 2 + pct3 * 3 + pct4 * 4 + pct5 * 5 + pct6 * 6 + pctx * 7) / 100
}

export const load_data_if_not = (fd) => {    
    if(Object.keys(fd).length==0){
        return d3.json('wordlestats_list.json')
    }
    else{
        return new Promise(function(resolve,reject){
            setTimeout(function(){
              resolve(fd);
            },1000)
          })
    }
}

export const transform_df_to_obj_array = (df) => {
    if(Object.keys(df).length>0){
        let newdf = {};
        let keylistx;
        let keylisty;
        keylisty = KEYLISTDEFAULTY;
        keylistx = KEYLISTDEFAULTX;
        for(let i in Object.keys(df)){
            let key = Object.keys(df)[i];
            if(!keylisty.includes(key) & !EXCLUDEKEY.includes(key)){
                keylisty.push(key)
            }
            if(!keylistx.includes(key) & !EXCLUDEKEYX.includes(key)){
                keylistx.push(key)
            }
            let newseries = [];
            for(let j in Object.keys(df[key])){
                let key2 = Object.keys(df[key])[j]
                newseries.push(df[key][key2]);
            }
            newdf[key] = newseries;
            if(key=='date'){
                newdf['date'] = newdf['date'].map(
                   (val, ind, arr) => {
                       return new Date(val*1000)
                   }
               )
            }
        }
        return {
            df: newdf,
            keylistx: keylistx,
            keylisty: keylisty   
        };
    }
}