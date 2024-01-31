<script>
    import polarbear from '$lib/images/PolarBear.png';
    import polarbear_stand from '$lib/images/PolarBear_stand.png';
    import anime from 'animejs/lib/anime.es.js';
    import { onMount } from 'svelte';

    import Graph1 from '$lib/components/graph_1.svelte';
    import Graph2 from '$lib/components/graph_2.svelte';
    import Graph3 from '$lib/components/graph_3.svelte';
    import Graph4 from '$lib/components/graph_4.svelte';
    import Graph5 from '$lib/components/graph_5.svelte';
    import Graph6 from '$lib/components/graph_6.svelte';

    import * as d3 from 'd3';

    $: scroll_position = 0;

    var animation = null;
    function animation_init() {
        animation = anime({
            targets: '.sprite > img',
            translateX: [304, -912],
            easing: "steps(4)",
            duration: 1000,
            loop: false,
            autoplay: false,
        });
    }

    function onscroll_animation() {
        document.addEventListener('wheel', function(e) {
            animation.play();

            console.log(scroll_position);

            if (scroll_position > 75) {
                scroll_position = 75;
            }

            if (scroll_position < 0) {
                scroll_position = 0;
            }

            if (e.deltaY > 0) {
                scroll_position++;
            } else {
                scroll_position--;
            }
        });
    }

    function clean_graph() {
        const graph = document.querySelector('svg');
        try {
            document.getElementsByClassName('input_range')[0].remove();
            document.getElementsByClassName('tooltip')[0].remove();
        } catch (error) {
            console.log("Everything is fine ;D");
        }
        d3.select(graph).selectAll('*').remove();
    }
    
    let rendered = false;
    onMount(() => {
        rendered = true;
        animation_init();
        onscroll_animation();
        new Graph1({
            target: document.querySelector('#graph'),
        });
    });


    function transitionGraph(newGraphConstructor, container) {
        const graphContainer = document.querySelector(container);


        const graph = document.querySelector('#graph');
        
        // Move current graph to the left
        graph.style.transform = 'translateX(-400%)';

        // Wait for the transition to complete
        setTimeout(() => {
            // Clean up the old graph
            clean_graph();

            // Reset the position for the new graph
            graph.style.transform = 'translateX(100%)';

            // Insert the new graph
            new newGraphConstructor({
                target: graphContainer,
            });

            // Slide in the new graph from the right
            setTimeout(() => {
                graph.style.transform = 'translateX(0)';
            }, 0); // Start immediately after the previous changes

        }, 500); // This duration should match the CSS transition time
    }


    let ice_width = 100;
    $: if (rendered) {
        if ((ice_width - scroll_position) > 20) {
            const ice = document.querySelector('.ice');
            if (ice_width - scroll_position < 100) {
                ice.style.width = ice_width - scroll_position + '%';
            } else {
                ice.style.width = '100%';
            }
        }

        if ((ice_width - scroll_position) <= 25) {
            const stand = document.querySelector('.stand');
            stand.style.display = 'block';

            const sprite = document.querySelector('.sprite');
            sprite.style.display = 'none';
        } else {
            const stand = document.querySelector('.stand');
            stand.style.display = 'none';

            const sprite = document.querySelector('.sprite');
            sprite.style.display = 'block';
        }


        if (scroll_position == -1) {
            transitionGraph(Graph1, '#graph');
        }

        if (scroll_position == 15) {
            transitionGraph(Graph2, 'body');
        }

        if (scroll_position == 30) {
            transitionGraph(Graph3, 'body');
        }

        if (scroll_position == 35) {
            transitionGraph(Graph4, '#graph');
        }

        if (scroll_position == 60) {
            transitionGraph(Graph5, '#graph');
        }

        if (scroll_position == 75) {
            transitionGraph(Graph6, '#graph');
        }


    }


</script>


<div class="home">

    <div class="sprite">
        <img src={polarbear} alt="polarbear" />
    </div>

    <div class="stand">
        <img src={polarbear_stand} alt="polarbear_stand" />
    </div>

    <div class="ice"></div>

    <div class="description">
        <p> ciao </p>
    </div>

    <svg id="graph"> </svg>

</div>

<style>

    .sprite {
        position: absolute;
        bottom: 2rem;
        left: 2rem;
        width: 304px;
        height: 205px;
        overflow: hidden;
    }

    .sprite > img {
    width: auto;
    height: 100%;
    }

    .ice {
        position: absolute;
        bottom: 1.5rem;
        left: 0;
        width: 100%;
        height: 2rem;
        background-color: #ffffff;
    }

    .stand {
        position: absolute;
        display: none;
        width: 304px;
        height: 205px;
        bottom: 3.1rem;
        left: 6rem;
        overflow: hidden;

    }

    .home {  
        background-color: #0d176d;
        color: #fff;
        height: 100vh;
        width: 100vw;
    }

    .description {
        width: 30rem;
        height: 66%;
        position: absolute;
        left: 0;
        top: 3rem;
        z-index: 400;
        background-color: #0d176d;
    }

    .description p {
        margin-left: 5rem;
        width: 25rem;
        font-size: 18px;

    }

    #graph {
        position: absolute;
        top: 2rem;
        right: 0;
        z-index: 100;
        display: block;
        margin-inline: auto;
        width: 60%;
        height: 40rem;
        transition: transform 1s ease-in-out;
    }   

</style>