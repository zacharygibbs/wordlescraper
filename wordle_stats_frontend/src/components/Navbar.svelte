<script>
    import {
        Collapse,
        Navbar,
        NavbarToggler,
        NavbarBrand,
        Nav,
        NavItem,
        NavLink,
        Dropdown,
        DropdownToggle,
        DropdownMenu,
        DropdownItem
    } from 'sveltestrap';
    import { Offcanvas, Modal } from 'sveltestrap';
    import {onMount} from 'svelte';
    let hostname = ''
    onMount(async () => {
        hostname = window.location.hostname;
	});
    

    const assemble_url = (route, hostname, subdir='')=>{//'wordle-stats-sciencey') => {
        if(hostname == 'localhost' | hostname == 'localhost:3000'){
            return route
        }
        else{
            return subdir + route
        }

    }

    // navbar variables
    let isOpen = false;
    function handleUpdate(event) {
        isOpen = event.detail.isOpen;
    }
    let open = false;
    const toggle = () => (open = !open);
</script>



<Navbar color="secondary" dark expand="md">
    <NavbarBrand href={"/wordle-stats-sciencey/"}>Wordle-Stats-Sciencey</NavbarBrand>
    <NavbarToggler on:click={() => (isOpen = !isOpen)} />
    <Collapse {isOpen} navbar expand="md" on:update={handleUpdate}>
        <Nav class="ms-auto" navbar>
        <NavItem>
            <NavLink href="/wordle-stats-sciencey/predict/nulls">Predictive Model</NavLink>
        </NavItem>
        <NavItem>
            <NavLink href="/wordle-stats-sciencey/distribution">Distribution</NavLink>
        </NavItem>
        <NavItem>
            <NavLink href="/wordle-stats-sciencey/charts">Charts</NavLink>
        </NavItem>
        <NavItem>
            <NavLink href="https://github.com/zacharygibbs/wordlescraper" target="_blank">GitHub</NavLink>
        </NavItem>
        <NavItem>
            <NavLink on:click={() => (open = !open)}>About</NavLink>
        </NavItem>
        </Nav>
    </Collapse>
</Navbar>

<Modal body header="About wordle-stats-sciencey" isOpen={open} {toggle} size='lg'>
    <div>
        Zach Gibbs, 2022 (GitHub - <a href="https://github.com/zacharygibbs/wordlescraper" target="_blank">zacharygibbs/wordlescraper</a>)<br>
        Application to gather and display daily wordle statistics as gathered from various sources.
        This application has three main tasks:
        <ul>
            <li>leverage data science model for predicting average word score ([<a href="https://github.com/zacharygibbs/wordlescraper/blob/main/WordleStatsAnalytics.ipynb">data science workup here</a>))</li>
            <li>compare user score distribution to global metrics as gathered by this app</li>
            <li>chart daily average score as a function of various word characterizers & time</li>
        </ul>
    </div>
    <div>
        <h6>References</h6>
        <div>
            Daily Wordle Statistics: <a href="https://twitter.com/wordlestats" target="_blank">@wordlestats</a> Twitter Bot<br>
            Daily Correct Words: <a href="http://screenrant.com/wordle-answers-updated-word-puzzle-guide/" target="_blank">screenrant.com</a> web page<br>
            English Word Frequency:  Kaggle - <a href="https://www.kaggle.com/datasets/rtatman/english-word-frequency" target="_blank">Rachael Tatman</a>
            All Wordle Wordlist: GitHub - csokolove <a href="https://github.com/csokolove/wordle-word-list" target="_blank">wordle-word-list</a><br>
        </div>
    </div>
    <div class="modal-div">
    <h6>Calculation Details</h6>
        <div>
            Note - "avg" metrics use 7 as numerical representation for number of guesses for "X", or if you do not get it correct.<br>
        </div>
    </div>
    <div class="modal-div">
        <span><img src="favicon.png" width="20" alt=''/><i>Created in Svelte</i></span> 
    </div>
    
</Modal>

<style>

    .modal-div{
        padding-top: 10px;
    }

</style>