<svelte:head>
    <!-- <link rel='stylesheet' href='chart.css'/> 
    <script src="https://cdn.plot.ly/plotly-2.12.1.min.js"></script>
    -->
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
    import {sum, dotprod} from './helpers.js'

    import { onMount } from "svelte";
    import { Styles, Col, Container, Row } from 'sveltestrap';
    import { Button, Input} from 'sveltestrap';
    import { Dropdown, DropdownItem, DropdownMenu, DropdownToggle } from 'sveltestrap';
    import * as d3 from 'd3';


    let df = {};
    let dfUser = {};
    let isMounted = false;
    onMount(async () => {
        if(Array.isArray(JSON.parse(localStorage.getItem('userStatsnum')))){
            userStatsnum = JSON.parse(localStorage.getItem('userStatsnum')); // undefined
        }
        else{
            userStatsnum = [0,0,0,1,0,0,0];
        }
        
        d3.json("wordlestats_list.json")
        //d3.json("http://coolsciencey.com/data/wordlestats_list.json")
        .then((data) =>{
                   console.log(data); // [{"Hello": "world"}, …]
                   df = data
                   // df.print() 
                 })
        isMounted=true;
	});

    $: {
        
        if(Object.keys(df).length>0){
            console.log(df)
            let newdf = {};
            for(let i in Object.keys(df)){
                let key = Object.keys(df)[i];
                let newseries = [];
                for(let j in Object.keys(df[key])){
                    let key2 = Object.keys(df[key])[j]
                    newseries.push(df[key][key2]);
                }
                newdf[key] = newseries;
            }
            df = newdf;
            avgStatsnum = statsNumbersstrs.map((val, ind) =>{
                return dotprod(df, 'pct_' + val, 'numresults') / 100
            })

            avgTotal = d3.sum(avgStatsnum)

            avgStatspct = avgStatsnum.map((val, ind) =>{
                return  val / avgTotal * 100
            })

        }
    }

    $: {
        if(isMounted){
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
                }
            };
            const PLOTLYDOM = document.getElementById('plotly-chart');
            Plotly.newPlot(PLOTLYDOM, data, layout);
        }
    }

    let statsNumbersstrs = ["1","2","3","4","5","6","X"];
    let statsNumbers = [1,2,3,4,5,6,7];
    let avgStatsnum = [0, 0, 0, 0, 0, 0, 0];
    let avgStatspct = [0, 0, 0, 0, 0, 0, 0];
    let avgTotal;
    let userStatsnum = [0, 0, 0, 1, 0, 0, 0];
    let userStatspct = [0, 0, 0, 0, 0, 0, 0];
    let userTotal;


    $:{
        if(isMounted){
            userTotal = sum(userStatsnum);
            localStorage.setItem('userStatsnum', JSON.stringify(userStatsnum));
        } 
    }

    $:{
        userStatspct = userStatsnum.map((x) => x / userTotal * 100);
    }



</script>
<Container>
    <Row>
        <h1>Wordle-Stats-Sciencey</h1>
        <br>
        <span><img src="favicon.png" width="20" alt=''/><i>Created in Svelte</i></span> 
        
    </Row>
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
                    <td></td>
                    <td></td>
                </tr>

            </table>
            <!-- <Button color="primary">butt</Button> -->
        </Col>
        <Col>
            <div id='plotly-chart' style="width:100%;height:90%;"></div>
            <!-- <div class="mb-3">
                <Dropdown>
                  <DropdownToggle caret>Date</DropdownToggle>
                  <DropdownMenu>
                    <DropdownItem>No Brush, No Lather</DropdownItem>
                  </DropdownMenu>
                </Dropdown> 
              </div> -->
        </Col>
        
    </Row>
</Container>
Data Source: <a href="https://twitter.com/wordlestats">@wordlestats</a> Twitter Account
<Styles></Styles>



<style>

    th, td {
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 30px;
    padding-right: 40px;
}


</style>