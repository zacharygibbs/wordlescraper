<svelte:head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>
</svelte:head>
<script>

    import { 
        sum, 
        dotprod, 
        calcAvg, 
        load_data_if_not,
        transform_df_to_obj_array
    } from './helpers.js'
    import { 
        df,
        isMounted,
    } from '../stores.js'
    import { onMount } from "svelte";
    import { Styles, Col, Container, Row } from 'sveltestrap';
    import { Button, Input, FormGroup, Label} from 'sveltestrap';
    import * as d3 from 'd3';

    $isMounted = false;

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
        load_data_if_not($df)
            .then((data) =>{
                console.log(data); // [{"Hello": "world"}, …]
                let result = transform_df_to_obj_array(data);
                $df = result['df']
            })
        $isMounted=true;
	});
    

    $: {
        if(Object.keys($df).length>0){
            avgStatsnum = statsNumbersstrs.map((val, ind) =>{
                return dotprod($df, 'pct_' + val, 'numresults') / 100
            })

            avgTotal = sum(avgStatsnum)

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

            let trace1_avg = {
                y: [userAvg, userAvg],
                x: [0, d3.max(userStatspct)],
                name: 'User Stats % avg',
                type: 'line',
            };

            let trace2 = {
                y: statsNumbers,
                x: avgStatspct,
                name: 'Global Stats %',
                type: 'bar',
                orientation: 'h'
            };

            let trace2_avg = {
                y: [avgAvg, avgAvg],
                x: [0, d3.max(avgStatspct)],
                name: 'Global Stats % avg',
                type: 'line',
            };

            let data = [trace1, trace2, trace1_avg, trace2_avg];

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
                    x: .8
                },
                displayModeBar: false
            };
            const PLOTLYDOM = document.getElementById('plotly-chart');
            Plotly.newPlot(PLOTLYDOM, data, layout);
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
    <Row width=100%>
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
            <div id='plotly-chart' style="width:100%;height:90%;"></div>
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