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
    var isTransitioning = false;
    var countdown = 5;

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
            if (!isTransitioning) {
                animation.play();

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
            }
        });
    }

    function clean_graph() {
        const graph = document.querySelector('svg');
        try {
            document.getElementsByClassName('input_range')[0].remove();
            document.getElementsByClassName('tooltip')[0].innerHTML = '';
        } catch (error) {
            console.log("Everything is fine ;D");
        }
        d3.select(graph).selectAll('*').remove();
    }
    
    let rendered = false;
    onMount(() => {


        let intervalcount = setInterval(() => {
            countdown--;
            if (countdown == 0) {
                clearInterval(intervalcount);
            }
        }, 1000);
        
        setTimeout(() => {
            const presentation = document.querySelector('.presentation');
            presentation.style.display = 'none';
        }, 5000);

        rendered = true;
        animation_init();
        onscroll_animation();
        new Graph1({
            target: document.querySelector('#graph'),
        });
    });


    function transitionGraph(newGraphConstructor, container) {
        isTransitioning = true;
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

            setTimeout(() => {
                isTransitioning = false;
            }, 1000); // This duration should match the CSS transition time
        }, 500); // This duration should match the CSS transition time
    }


    let ice_width = 100;
    let percent = 100;
    var foo = 0;
    $: if (rendered) {

        document.querySelector('.percent').style.left = ice_width * 0.92 + '%';

        foo = Math.floor(ice_width - scroll_position * 1.33);
        
        if (foo < 0) {
            percent = 0 + '%';
        } else if (foo > 100) {
            percent = 100 + '%';
        } else {
            percent = foo + '%';
        }


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

        if (scroll_position == 45) {
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


<div class="presentation">

    <div class="countdown"> {countdown} </div>

    <img src={polarbear_stand} alt="Polar bear stand">

    <p> The goal of this project is to showcase the causes and effects of climate change, particularly in Europe. To scroll through the charts, you need to move the mouse wheel forward and backward. It is recommended to reduce the browser zoom, usually to 75%/90%, if the visualizations are not clear or if the cursor goes over the text or charts. This issue does not occur on larger screens. </p>

</div>

<div class="home">

    <div class="sprite">
        <img src={polarbear} alt="polarbear" />
    </div>

    <div class="stand">
        <img src={polarbear_stand} alt="polarbear_stand" />
    </div>

    <div class="ice">

        <p class="percent"> {percent} </p>

    </div>

    <div class="hide"></div>

    <div class="description">
        <p> ciao </p>
    </div>

    <svg id="graph"> </svg>

    <div id="tooltip" class="tooltip"></div>

</div>

<style>

    .presentation {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #0d176d;
        z-index: 5000;
        color: white;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: opacity 2s ease-in-out;
    }

    .presentation p {
        margin-top: 5rem;
        width: 40rem;
        font-size: 20px;
        text-align: center;
    }

    .sprite {
        position: absolute;
        bottom: 2rem;
        left: 2rem;
        width: 304px;
        height: 205px;
        overflow: hidden;
        z-index: 150;
    }

    .sprite > img {
        width: auto;
        height: 100%;
        z-index: 151;
    }

    .ice {
        position: absolute;
        bottom: 1.5rem;
        left: 0;
        width: 100%;
        height: 2rem;
        background-color: #ffffff;
        z-index: 155;
    }

    .percent {
        position: absolute;
        text-align: center;
        top: 3px;
        color: black;
        font-size: 20px;
    }

    .stand {
        position: absolute;
        display: none;
        width: 304px;
        height: 205px;
        bottom: 3.1rem;
        left: 6rem;
        overflow: hidden;
        z-index: 151;

    }

    .home {  
        background-color: #0d176d;
        color: #fff;
        height: 100vh;
        width: 100vw;
    }

    .description {
        width: 30rem;
        height: max-content;
        position: absolute;
        left: 0;
        z-index: 400;
        background-color: #0d176d;
    }

    .description p {
        margin-top: 3rem;
        margin-left: 5rem;
        width: 25rem;
        font-size: 18px;

    }

    .hide {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 30rem;
        height: 100rem;
        background-color: #0d176d;
        z-index: 140;
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


    .tooltip {
        position: absolute;
        text-align: left;
        width: auto;
        height: auto;
        padding: 10px;
        background: rgba(0, 0, 0, 0.9);
        border: 0px;
        border-radius: 4px;
        opacity: 0;
        color: #fff;
        z-index: 3000;
    }

    .countdown {
        font-size: 42px;
        margin-bottom: 5rem;
    }



    @media screen and (max-width: 1600px) {
        .sprite {
            transform: scale(0.7);
            bottom: -0.1rem;
        }

        .stand {
            transform: scale(0.7);
            bottom: 0.2rem;
        }

        .ice {
            height: 1.5rem;
            bottom: 1rem;
        }

        .description p {
            font-size: 18px;
        }

        #graph {
            width: 58%;
            height: 38rem;
        }
    }

    @media screen and (max-width: 1400px) {
        .sprite{
            transform: scale(0.55);
            bottom: -1rem;
        }

        .stand {
            transform: scale(0.55);
            bottom: -1rem;
        }

        .ice {
            height: 1.5rem;
            bottom: 1rem;
        }

        .description p {
            font-size: 17px;
        }

        #graph {
            width: 58%;
            height: 38rem;
        }
    }


    @media screen and (max-height: 700px) {
        .sprite{
            transform: scale(0.5);
            bottom: -2rem;
        }

        .stand {
            transform: scale(0.5);
            bottom: -2rem;
        }

        .ice {
            height: 1.5rem;
            bottom: 0.5rem;
        }

        .description p {
            font-size: 15px;
        }

        .description {
            width: 10rem;
        }

        #graph {
            width: 60%;
            height: 32rem;
        }
    }


</style>