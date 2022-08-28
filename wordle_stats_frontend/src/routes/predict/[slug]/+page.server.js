import * as d3 from 'd3';
import { error } from '@sveltejs/kit';
import { 
    load_data_if_not,
    transform_df_to_obj_array, 
    CHARTMODE
} from '$lib/helpers'

import { 
    df,
    isMounted,
} from '../../../stores.js'

const URL = 'https://infinite-temple-05275.herokuapp.com/';//wordleword/brick
const URL_LOCALHOST = 'http://localhost:8000/'
//

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    let hostname = 'localhost'//window.location.hostname
    let urlChosen = hostname=='localhost' ? URL_LOCALHOST : URL 
    //return d3.json(urlChosen + 'wordleword/' + wordleword)
    // Default options are marked with *
    console.log(df);
    let responsefunc;
    df.subscribe(data => {
        ( responsefunc = async () => {
            let newdf1 = {};    
            await load_data_if_not(data).then((newdata) =>{
                newdf1 = transform_df_to_obj_array(newdata);
            })
            return newdf1;
            }
        )()
    });
    let responsedf = await responsefunc()
    let newdf = responsedf['df']
    let res;
    await fetch(urlChosen + 'wordleword/' + params.slug, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        headers: {
        'Content-Type': 'application/json'
        },
    }).then(response => 
        response.json().then(data => {
            res = data;
            return {
                data: data,
                status: response.status
            }
        })
        ).then(resp => {
            console.log(resp.status, resp.data)
    });
    //console.log(res);
    //console.log({predict: res, df: newdf})
    newdf.date = newdf.date.map(v => v.toJSON());
    return {predict: res, df: newdf};
  throw error(404, 'Not found');
  
}


