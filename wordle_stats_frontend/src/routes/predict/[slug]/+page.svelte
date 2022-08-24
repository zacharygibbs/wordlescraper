<svelte:head>
    
    <script src="https://cdn.plot.ly/plotly-2.14.0.min.js"></script>
</svelte:head>

<script>
    /** @type {import('./$types').PageData} */
    export let data;
    /*
    Called index, but this is the predictive model
    want to have Text entry for user w/ submit button to get avg estimated, also return if that word has ever
    been used, what date, an what the score was
    Also, include chart w/ data poitns for predictors and highlighted point showing where this new word is.
    */
    import { 
        load_data_if_not,
        transform_df_to_obj_array, 
        CHARTMODE
    } from '../../helpers.js'

    import { 
        df,
        isMounted,
    } from '../../../stores.js'


    import { onMount } from "svelte";
    import { Styles, Col, Container, Row } from 'sveltestrap';
    import { Button, Input, FormGroup, Label} from 'sveltestrap';
    import { Spinner, Icon } from 'sveltestrap';
    import { Table } from 'sveltestrap';

    import * as d3 from 'd3';

    import { page } from '$app/stores';

    import { goto } from '$app/navigation';

    //import Plotly from 'plotly.js-dist-min'

    function routeToPage(route, replaceState) {
        goto(`${route}`, { replaceState }) 
    }

    $: {
        if($isMounted){
            data;
            validate_submit();
        }
    }

    $isMounted = false;
    
    let enteredWord = $page.params.slug;
    let isLoading = false;
    let apiResult = {};
    let errorPredicted = '';
    let isValid = false;
    let find_word = [];
    
    const CHARTITEMS = ['avg', 'logfreq', 'scrabblescore', 'duplicate_letters'];

    onMount(async () => {
        load_data_if_not($df)
            .then((data) =>{
                let result = transform_df_to_obj_array(data);
                $df = result['df']
                console.log($df)
            })
        $isMounted=true;
        validate_submit()
	});

    const handleKeydown = (event) => {
        if(event.key=='Enter'){
            validate_submit()
        }
    }

    const update_chart = () => {
        if($isMounted){
            CHARTITEMS.forEach((selectedItemCharty, index, arr) => {
                //let selectedItemCharty = 'avg'
                let charttype ='box';
                let jitter = 0.3;
                let pointpos = -1.8;
                let boxpoints = 'all';
                let trace1 = {
                    y: $df[selectedItemCharty],
                    text: $df['wordleword'],
                    mode: CHARTMODE,
                    type: charttype,
                    name: selectedItemCharty,
                    boxpoints: boxpoints,
                    jitter: jitter,
                    pointpos: pointpos
                };
                let data;
                let trace2;
                let predictedResult = apiResult[selectedItemCharty + (selectedItemCharty=='avg' ? '_predicted' : '')];
                if(selectedItemCharty == 'avg'){
                    trace2 = {
                        y: $df[selectedItemCharty+'_predicted'],
                        text: $df['wordleword'],
                        mode: CHARTMODE,
                        type: charttype,
                        name: 'Predicted',
                        boxpoints: boxpoints,
                        jitter: jitter,
                        pointpos: pointpos
                    };
                    data = [trace1, trace2];//, tracePred];
                }
                else{
                    data = [trace1];//, tracePred];
                }

                let layout = {
                    yaxis: {
                        title: selectedItemCharty == 'avg' ? 'Average Wordle Score' : selectedItemCharty
                    },
                    title: enteredWord.toUpperCase(),
                    displayModeBar: false,
                    shapes: [
                                {
                                    type: 'line',
                                    xref: 'paper',
                                    x0: 0,
                                    y0: predictedResult,
                                    x1: 1,
                                    y1: predictedResult,
                                    line:{
                                        color: 'rgb(255, 0, 0)',
                                        width: 4,
                                        dash:'dot'
                                    },
                                }
                            ]
                };
                Plotly.purge('plotly-chart-' + selectedItemCharty)
                const PLOTLYDOMTIME = document.getElementById('plotly-chart-' + selectedItemCharty);
                Plotly.newPlot(PLOTLYDOMTIME, data, layout);
            })
        }
    }

const validate_submit = () =>{
    if($isMounted){
        console.log(enteredWord)
        if(enteredWord!==$page.params.slug){
            routeToPage(enteredWord, true)
        }
        isLoading = true;
        //getPrediction(enteredWord, window.location.hostname).then(data => {
        apiResult = JSON.parse(
            Object.keys(data).reduce(
                            (prev, cur, index) => {
                                        return prev + data[Object.keys(data)[index]]
                                    }, '')
        );
        isLoading = false;
        errorPredicted = '';
        if(apiResult.hasOwnProperty('Error')){
            errorPredicted = apiResult['Error'];
        }
        //{"wordleword":"GLADE","freq":1168016,"logfreq":6.067448792,"letter_matches_2":742.0,"letter_matches_3":359.0,"letter_matches_4":66.0,"letter_matches_5":7.0,"duplicate_letters":0.0,"scrabblescore":7,"num_vowels":2,"starts_with_vowel":0,"avg_predicted":4.0544637434}
        console.log(apiResult)
        isValid = apiResult!={} && !apiResult.hasOwnProperty('Error')
        console.log($df['wordleword'])
        if(isValid){
            update_chart();
            find_word = $df['wordleword'].reduce((prev, cur, index) =>{
                if($df['wordleword'][index].toUpperCase() == enteredWord.toUpperCase()){
                    return [...prev, $df['avg'][index]]
                }
                else{
                    return prev
                }
            }, [])
            console.log(find_word)
        }
    }

}

</script>

<Container>
    <Row>
        <b>Instructions:</b> Type a 5 letter word, if it's in the wordle word list, will return Predicted Avg Score along with the predictor values used in the model. <br>
        logfreq - frequency of word's use in english language<br>
        scrabblescore - number of points the word would give in Scrabble<br>
        duplicate_letters - how many sets of duplicate letters the word has<br>
    </Row>
    <Row>
        <Col xs="7" scrolly="false">
            <FormGroup>
                <input type="text" bind:value={enteredWord} minlength="5" maxlength="5" on:keydown={handleKeydown}/>
                <Button on:click={validate_submit}>Submit</Button>
                {#if isLoading}
                    <Spinner color="primary" /> Loading - Can take 10 or 15 seconds<br>    
                {/if}
                <br>
                <span class="error-message-prediction">{errorPredicted}</span><br>
            </FormGroup>

            <Table dark bordered>
                <thead>
                    <th>Metric</th>
                    <th>avg Observed</th>
                    <th>avg_predicted</th>
                    <th>logfreq</th>
                    <th>scrabblescore</th>
                    <th>duplicateletters</th>
                </thead>
                <tr>
                    <td>
                        {#if isValid}
                            {apiResult['wordleword']}
                        {/if}
                    </td>
                    <td>
                        {#if find_word.length > 0 }
                            {find_word[0].toFixed(2)}
                        {/if}
                    </td>
                    <td>
                        {#if isValid}
                            {apiResult['avg_predicted'].toFixed(2)}
                        {:else}
                            N/A
                        {/if}
                    </td>
                    <td>
                        {#if isValid}
                            {apiResult['logfreq'].toFixed(1)}
                        {:else}
                            N/A
                        {/if}
                    </td>
                    <td>
                        {#if isValid}
                            {apiResult['scrabblescore']}
                        {:else}
                            N/A
                        {/if}
                    </td>
                    <td>
                        {#if isValid}
                            {apiResult['duplicate_letters']}
                        {:else}
                            N/A
                        {/if}
                    </td>
                </tr>
                <tr>
                    <td>Max</td>
                    {#if $isMounted &&  Object.keys($df).length>0}
                        <td>{d3.max($df['avg']).toFixed(2)}</td>
                        <td>{d3.max($df['avg_predicted']).toFixed(2)}</td>
                        <td>{d3.max($df['logfreq']).toFixed(1)}</td>
                        <td>{d3.max($df['scrabblescore'])}</td>
                        <td>{d3.max($df['duplicate_letters'])}</td>
                    {/if}
                </tr>
                <tr>
                    <td>Avg</td>
                    {#if $isMounted && Object.keys($df).length>0}
                        <td>{d3.mean($df['avg']).toFixed(2)}</td>
                        <td>{d3.mean($df['avg_predicted']).toFixed(2)}</td>
                        <td>{d3.mean($df['logfreq']).toFixed(1)}</td>
                        <td>{d3.mean($df['scrabblescore']).toFixed(1)}</td>
                        <td>{d3.mean($df['duplicate_letters']).toFixed(1)}</td>
                    {/if}
                </tr>
                <tr>
                    <td>Min</td>
                    {#if $isMounted && Object.keys($df).length>0}
                        <td>{d3.min($df['avg']).toFixed(2)}</td>
                        <td>{d3.min($df['avg_predicted']).toFixed(2)}</td>
                        <td>{d3.min($df['logfreq']).toFixed(1)}</td>
                        <td>{d3.min($df['scrabblescore'])}</td>
                        <td>{d3.min($df['duplicate_letters'])}</td>
                    {/if}
                </tr>
            
            </Table>

            {#each CHARTITEMS as chartitem, index}
                <Row>
                    <Col>
                        <div id={'plotly-chart-'+chartitem} style="width:100%;height:90%;"></div>
                    </Col>    
                </Row>
            {/each}
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
    .error-message-prediction{
        color:red;
        font-style: italic;
    }
</style>