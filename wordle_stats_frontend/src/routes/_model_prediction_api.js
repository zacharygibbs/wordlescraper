import * as d3 from 'd3';

const URL = 'https://infinite-temple-05275.herokuapp.com/';//wordleword/brick

export const getPrediction = (wordleword) => {
    return d3.json(URL + '/wordleword/' + wordleword)
}
