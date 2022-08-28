<svelte:head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>
</svelte:head>

<script>
    import { 
        setSelectedValue, 
        load_data_if_not,
        transform_df_to_obj_array,
        CHARTMODE
    } from '$lib/helpers.js'

    import { 
        df,
        isMounted,
    } from '../../stores.js'

    import { onMount } from "svelte";
    import { Styles, Col, Container, Row } from 'sveltestrap';
    import { Button, Input, FormGroup, Label} from 'sveltestrap';
    import { TabContent, TabPane } from 'sveltestrap';


    $isMounted = false;
    
    let selectedItemChartx = null;
    let selectedItemCharty = null;
    const VIOLINVARS = ['duplicate_letters', 'num_vowels', 'starts_with_vowel'];
    let keylistx = [];
    let keylisty = [];
    

    onMount(async () => {
        $isMounted = true;
        load_data_if_not($df)
            .then((data) =>{
                console.log(data); // [{"Hello": "world"}, …]
                let result = transform_df_to_obj_array(data);
                $df = result['df']
                keylistx = result['keylistx']
                keylisty = result['keylisty']
                selectedItemCharty = 'avg';
                selectedItemChartx = 'wordleid';
            })
            
        updateValue()
	});

    function updateValue() {
        let fsy = document.getElementById('form-selecty')
        setSelectedValue(fsy, 'avg');
        let fsx = document.getElementById('form-selectx')
        setSelectedValue(fsx, 'wordleid');
    }

    
    

    $: {
        
    }  
    
   /* {
    y: [0, 1, 1, 2, 3, 5, 8, 13, 21],
    boxpoints: 'all',
    jitter: 0.3,
    pointpos: -1.8,
    type: 'box'
  }*/

    $: {
        if($isMounted){
            let charttype
            let jitter = 0;
            let boxpoints = 'all'
            let pointpos = 0;
            if(VIOLINVARS.includes(selectedItemChartx)){
                charttype ='box';
                jitter = 0.3;
                pointpos = -1.8;
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
                name: 'Global',
                boxpoints: boxpoints,
                jitter: jitter,
                pointpos: pointpos
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
                    name: 'Predicted',
                    boxpoints: boxpoints,
                    jitter: jitter,
                    pointpos: pointpos
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



</script>

<Container>
    <Row>
        <Col>
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
        </Col>
    </Row>
    <Row>
        <div id='plotly-chart-time' style="width:100%;height:90%;"></div>
    </Row>
</Container>