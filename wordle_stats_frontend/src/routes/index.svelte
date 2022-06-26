<svelte:head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>
</svelte:head>

<script>
    /*
    Called index, but this is the predictive model
    want to have Text entry for user w/ submit button to get avg estimated, also return if that word has ever
    been used, what date, an what the score was
    Also, include chart w/ data poitns for predictors and highlighted point showing where this new word is.
    */
    import { 
        load_data_if_not,
        transform_df_to_obj_array 
    } from './helpers.js'

    import { 
        df,
        isMounted,
    } from '../stores.js'

    import {
        getPrediction
    } from './_model_prediction_api'

    import { onMount } from "svelte";
    import { Styles, Col, Container, Row } from 'sveltestrap';
    import { Button, Input, FormGroup, Label} from 'sveltestrap';
    import { Spinner } from 'sveltestrap';

    import * as d3 from 'd3';

    $isMounted = false;
    
    let enteredWord;
    let isLoading = false;
    let scorePredicted;
    let apiResult;

    onMount(async () => {
        load_data_if_not($df)
            .then((data) =>{
                console.log(data); // [{"Hello": "world"}, …]
                let result = transform_df_to_obj_array(data);
                $df = result['df']
            })
        $isMounted=true;
	});

/*    $: {
        if(Object.keys($df).length>0){
            let newdf = {};
            keylisty = KEYLISTDEFAULTY;
            keylistx = KEYLISTDEFAULTX;
            for(let i in Object.keys($df)){
                let key = Object.keys($df)[i];
                if(!keylisty.includes(key) & !EXCLUDEKEY.includes(key)){
                    keylisty.push(key)
                }
                if(!keylistx.includes(key) & !EXCLUDEKEYX.includes(key)){
                    keylistx.push(key)
                }
                let newseries = [];
                for(let j in Object.keys($df[key])){
                    let key2 = Object.keys($df[key])[j]
                    newseries.push($df[key][key2]);
                }
                newdf[key] = newseries;
                if(key=='date'){
                    console.log(newdf['date'])
                    newdf['date'] = newdf['date'].map(
                       (val, ind, arr) => {
                           return new Date(val*1000)
                       }
                   )
                }
            }
            $df = newdf;
            avgStatsnum = statsNumbersstrs.map((val, ind) =>{
                return dotprod($df, 'pct_' + val, 'numresults') / 100
            })

            avgTotal = d3.sum(avgStatsnum)

            avgStatspct = avgStatsnum.map((val, ind) =>{
                return  val / avgTotal * 100
            })

        }
    }

    $: {
        if($isMounted){
            let trace1 = {
                y: statsNumbers,
                x: userStatspct,
                name: 'User Stats %',
                type: 'bar',
                orientation: 'h'
            };

            let trace2 = {
                y: statsNumbers,
                x: avgStatspct,
                name: 'Global Stats %',
                type: 'bar',
                orientation: 'h'
            };

            let data = [trace1, trace2];

            let layout = {
                barmode: 'group',
                xaxis: {
                    title: '% Occurence'
                },
                yaxis: {
                    title: 'Number of Guesses',
                    autorange: 'reversed',
                    tickmode: 'array',
                    tickvals: [1, 2, 3, 4, 5, 6, 7],
                    ticktext: ['1  ', '2  ', '3  ', '4  ', '5  ', '6  ', 'X  ']
                },
                title: 'User vs Global ' + 'ALL',
                legend: {
                    orientation:"h",
                    yanchor: "bottom",
                    y: 1.02,
                    xanchor: "right",
                    x: .5
                },
                displayModeBar: false
            };
            const PLOTLYDOM = document.getElementById('plotly-chart');
            Plotly.newPlot(PLOTLYDOM, data, layout);
        }
    }
*/

const validate_submit = () =>{
    console.log(enteredWord)
    isLoading = true;
    getPrediction(enteredWord).then(data => {
        apiResult = data;
        isLoading = false;
    })

    console.log(apiResult)


}


</script>

<Container>
    <Row>
        <Col xs="5">
            <FormGroup>
                <input type="text" bind:value={enteredWord} minlength="5" maxlength="5"/>
                <Button on:click={validate_submit}>Submit</Button>
            </FormGroup>
            {#if isLoading}
                <Spinner color="primary" /> Loading - Can take 10 or 15 seconds
                
        {/if}
        </Col>
        <Col>
            Second Column
        </Col>    
    </Row>
</Container>

<style>
    input {
        border: 0px solid currentcolor;
    }
    input:focus {
        border: 0px solid currentcolor;
    }
    input:invalid {
        border: 2px solid red;
    }
    input:invalid:focus {
        border: 2px solid red;
    }
</style>