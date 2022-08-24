import * as d3 from 'd3';

const URL = 'https://infinite-temple-05275.herokuapp.com/';//wordleword/brick
const URL_LOCALHOST = 'http://localhost:8000/'
//


export const getPrediction = (wordleword, hostname) => {
    let urlChosen = hostname=='localhost' ? URL_LOCALHOST : URL 
    return d3.json(urlChosen + 'wordleword/' + wordleword)
}
