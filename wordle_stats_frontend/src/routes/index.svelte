<svelte:head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>
</svelte:head>

<script>
    // possible things to do
    //  add 'average' line for User and Global stats
    //  add distrib?
    //  add average / skewness?
    //  add dropdown to choose date, will show word and date
    //  add cookie to remember user stats?   
    // time series chart to show distribution 
    // get better worlde winne website (https://screenrant.com/wordle-answers-updated-word-puzzle-guide/)
    import { sum, dotprod, setSelectedValue, calcAvg } from './helpers.js'

    import { onMount } from "svelte";
    import { Styles, Col, Container, Row } from 'sveltestrap';
    import { Button, Input, FormGroup, Label} from 'sveltestrap';
    import { TabContent, TabPane } from 'sveltestrap';

    import * as d3 from 'd3';
    //import * as Statistics from 'statistics';
    import { 
        df,
        isMounted,

    } from '../stores.js'
    
    // main variables
    //let df = {};// store
    // - charts.svelte
    let selectedItemChartx = null;
    let selectedItemCharty = null;
    const KEYLISTDEFAULTY = ['avg', 'stddev', 'pctCG_good', 'pctCG_medium', 'pctCG_bad'];
    let keylisty = KEYLISTDEFAULTY;
    const EXCLUDEKEY = ['wordleid', 'wordleword', 'date', 'index'];
    const KEYLISTDEFAULTX = ['wordleid', 'logfreq', 'scrabblescore', 'duplicate_letters', 'letter_matches_2', 'letter_matches_3', 'letter_matches_4', 'letter_matches_5', 'num_vowels', 'starts_with_vowel', 'freq'];
    let keylistx = KEYLISTDEFAULTX;
    const EXCLUDEKEYX = ['date', 'index', 'avg', 'stddev', 'pctCG_good', 'pctCG_medium', 'pctCG_bad', 'pct_1', 'pct_2', 'pct_3', 'pct_4', 'pct_5', 'pct_6', 'pct_X'];
    const CHARTMODE = 'markers';
    const VIOLINVARS = ['duplicate_letters', 'num_vowels', 'starts_with_vowel'];

    // - distribution.svelte
    let userAvg;
    let avgAvg;
    let statsNumbersstrs = ["1","2","3","4","5","6","X"];
    let statsNumbers = [1,2,3,4,5,6,7];
    let avgStatsnum = [0, 0, 0, 0, 0, 0, 0];
    let avgStatspct = [0, 0, 0, 0, 0, 0, 0];
    let avgTotal;
    let userStatsnum = [0, 0, 0, 1, 0, 0, 0];
    let userStatspct = [0, 0, 0, 0, 0, 0, 0];
    let userTotal;
    

    onMount(async () => {
        if(Array.isArray(JSON.parse(localStorage.getItem('userStatsnum')))){
            userStatsnum = JSON.parse(localStorage.getItem('userStatsnum')); // undefined
        }
        else{
            userStatsnum = [0,0,0,1,0,0,0];
        }
        
        d3.json('wordlestats_list.json')
        //d3.json("http://coolsciencey.com/data/wordlestats_list.json")
        .then((data) =>{
                   console.log(data); // [{"Hello": "world"}, …]
                   $df = data;
                 })
        $isMounted=true;
        selectedItemCharty = 'avg';
        selectedItemChartx = 'wordleid';
        updateValue()
	});

    function updateValue() {
        let fsy = document.getElementById('form-selecty')
        setSelectedValue(fsy, 'avg');
        let fsx = document.getElementById('form-selectx')
        setSelectedValue(fsx, 'wordleid');
    }

    
    

    $: {
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

    $: {
        if($isMounted){
            let charttype
            if(VIOLINVARS.includes(selectedItemChartx)){
                charttype ='violin'
            }
            else{
                charttype = 'scatter'
            }
            let trace1 = {
                x: $df[selectedItemChartx],
                y: $df[selectedItemCharty],
                text: $df['wordleword'],
                mode: CHARTMODE,
                type: charttype,
                name: 'Global'
            };
            let data;
            let trace2;
            if(keylisty.includes(selectedItemCharty+'_predicted')){
                trace2 = {
                    x: $df[selectedItemChartx],
                    y: $df[selectedItemCharty+'_predicted'],
                    text: $df['wordleword'],
                    mode: CHARTMODE,
                    type: charttype,
                    name: 'Predicted'
                };
                data = [trace1, trace2];
            }
            else{
                data = [trace1];
            }

            

            let layout = {
                xaxis: {
                    title: selectedItemChartx
                },
                yaxis: {
                    title: selectedItemCharty
                },
                title: '',
                displayModeBar: false
            };
            const PLOTLYDOMTIME = document.getElementById('plotly-chart-time');
            Plotly.newPlot(PLOTLYDOMTIME, data, layout);
        }
    }

    $:{
        if($isMounted){
            userTotal = sum(userStatsnum);
            localStorage.setItem('userStatsnum', JSON.stringify(userStatsnum));
        } 
    }

    $:{
        userStatspct = userStatsnum.map((x) => x / userTotal * 100);
    }

    $: userAvg = calcAvg(...userStatspct)
    $: avgAvg = calcAvg(...avgStatspct)



</script>
<Container>
    <Row>
        <Col>
            <table>
                <tr>
                    <th># of Guesses</th>
                    <th>User Stats</th> 
                    <th>User Stats %</th> 
                    <th>Global Stats %</th> 
                </tr>
                {#each statsNumbersstrs as num, index}
                    <tr>
                        <td>{num}</td>
                        <td>
                            <Input
                                type="number"
                                name='number{num}'
                                id="statsNumber{num}"
                                placeholder="number of {num}'s"
                                bind:value={userStatsnum[index]}
                            />
                        </td>
                        <td>{userStatspct[index].toFixed(1)}</td>
                        <td>{avgStatspct[index].toFixed(1)}</td>
                    </tr>
                {/each}
                <tr>
                    <td></td>
                    <td>Total: {userTotal}</td>
                    <td>Avg: {userAvg.toFixed(2)}</td>
                    <td>Avg: {avgAvg.toFixed(2)}</td>
                </tr>

            </table>
            <!-- <Button color="primary">butt</Button> -->
        </Col>
        <Col>
            <TabContent pills>
                <TabPane tabId="tab-score-dist" tab="Score Distribution" active>
                    <div id='plotly-chart' style="width:100%;height:90%;"></div>
                    <!-- <div class="mb-3">
                        <Dropdown>
                        <DropdownToggle caret>Date</DropdownToggle>
                        <DropdownMenu>
                            <DropdownItem>No Brush, No Lather</DropdownItem>
                        </DropdownMenu>
                        </Dropdown> 
                    </div> -->
                </TabPane>
                <TabPane tabId="tab-time" tab="Charts">
                    <FormGroup>
                        <Row>
                            <Col>
                                <Label for="form-selecty">Select y</Label>
                                <Input type="select" name="form-selecty" id="form-selecty" bind:value={selectedItemCharty}>
                                    {#each keylisty as key}
                                        <option>{key}</option>
                                    {/each}
                                </Input>
                            </Col>
                            <Col>
                                <Label for="form-selectx">Select x</Label>
                                <Input type="select" name="form-selectx" id="form-selectx" bind:value={selectedItemChartx}>
                                    {#each keylistx as key}
                                        <option>{key}</option>
                                    {/each}
                                </Input>
                            </Col>
                        </Row>
                      </FormGroup>
                        
                    <div id='plotly-chart-time' style="width:100%;height:90%;"></div>
                </TabPane>
            </TabContent>

        </Col>
        
    </Row>
</Container>
<!-- <Styles/> -->



<style>

    th, td {
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 30px;
    padding-right: 40px;
}



</style>