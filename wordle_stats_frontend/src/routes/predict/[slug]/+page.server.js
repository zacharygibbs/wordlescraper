import * as d3 from 'd3';
import { error } from '@sveltejs/kit';

const URL = 'https://infinite-temple-05275.herokuapp.com/';//wordleword/brick
const URL_LOCALHOST = 'http://localhost:8000/'
//


export const getPrediction = (wordleword) => {

}

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    let hostname = 'localhost'//window.location.hostname
    let urlChosen = hostname=='localhost' ? URL_LOCALHOST : URL 
    //return d3.json(urlChosen + 'wordleword/' + wordleword)
    // Default options are marked with *
    const response = await fetch(urlChosen + 'wordleword/' + params.slug, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        headers: {
        'Content-Type': 'application/json'
        },
    });
  if (response) {
    let res = response.json()
    return res;
  }
  throw error(404, 'Not found');
}