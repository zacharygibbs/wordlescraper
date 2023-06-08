import * as d3 from 'd3';
import { error } from '@sveltejs/kit';
import { 
    load_data_if_not,
    transform_df_to_obj_array, 
    CHARTMODE
} from '$lib/helpers'

const URL = 'https://infinite-temple-05275.herokuapp.com/';//wordleword/brick
const URL_LOCALHOST = 'http://localhost:8000/'
//

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    let hostname = 'localhost'//window.location.hostname
    let urlChosen = hostname=='localhost' ? URL_LOCALHOST : URL 
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
    return {predict: res};
  throw error(404, 'Not found');
  
}


