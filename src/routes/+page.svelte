<script>
    import { base } from '$app/paths';
    import polarbear from '$lib/images/PolarBear.png';
    import polarbear_stand from '$lib/images/PolarBear_stand.png';
    import anime from 'animejs/lib/anime.es.js';
    import { onMount } from 'svelte';
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
            if (e.deltaY > 0) {
                scroll_position++;
            } else {
                scroll_position--;
            }
        });
    }

    function example_graph() {
        // Sample data: an array of objects with x and y properties
        const data = [
                { x: 30, y: 30 },
                { x: 70, y: 70 },
                { x: 110, y: 100 },
                { x: 140, y: 110 },
                { x: 170, y: 150 },
                // Add more data points as needed
            ];

            // SVG dimensions
            const width = 500;
            const height = 500;
            const margin = { top: 20, right: 20, bottom: 60, left: 40 };

            // Create scale functions
            const xScale = d3.scaleLinear()
                            .domain([0, d3.max(data, d => d.x)]) // Input
                            .range([margin.left, width - margin.right]); // Output

            const yScale = d3.scaleLinear()
                            .domain([0, d3.max(data, d => d.y)]) // Input
                            .range([height - margin.bottom, margin.top]); // Output

            // Create SVG element
            const svg = d3.select('.graph')
                        .append('svg')
                        .attr('width', width)
                        .attr('height', height);

            // Create points
            svg.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr('cx', d => xScale(d.x))
            .attr('cy', d => yScale(d.y))
            .attr('fill', 'white')
            .attr('r', 5);

            // Create axes
            svg.append('g')
            .attr('transform', `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(xScale));

            svg.append('g')
            .attr('transform', `translate(${margin.left},0)`)
            .call(d3.axisLeft(yScale));   

    }

    
    let rendered = false;
    onMount(() => {
        rendered = true;
        animation_init();
        onscroll_animation();
        example_graph();
    });


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

        if ((ice_width - scroll_position) <= 20) {
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

    <p class="description">
        Lorem ipsum, dolor sit amet consectetur adipisicing elit. Recusandae, ipsam asperiores. Tempora dolore fugit dolorem est officiis maxime, deserunt asperiores? Dolorum expedita earum fugiat accusamus placeat perspiciatis ratione reiciendis, odit omnis consectetur blanditiis et aspernatur ab nobis ex aliquam eius necessitatibus odio quisquam sed at unde! Velit optio odio maiores fugit eligendi ducimus officia commodi pariatur, est nesciunt ullam voluptatem itaque aliquam sit unde cupiditate, veniam asperiores? Laboriosam accusantium officia nemo voluptatum mollitia. Fuga dolorum mollitia voluptatum aperiam, blanditiis, culpa cupiditate quasi saepe maxime, quaerat sequi nam quos ipsam neque! Eaque illo reiciendis error in obcaecati perferendis fugit corporis porro perspiciatis? Dicta similique, iure nobis rem in iste obcaecati aliquid quos deserunt vel eos autem quaerat aliquam distinctio voluptates doloribus, sequi iusto. Natus sapiente assumenda, est sed molestiae suscipit nihil aspernatur placeat praesentium? Perferendis iure reprehenderit, error rerum corporis facilis.
    </p>

    <div class="graph">
        <svg> </svg>
    </div>

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
        background-color: #202eb3;
        color: #fff;
        height: 100vh;
        width: 100vw;
    }

    .description {
        font-size: 18px;
        width: 25rem;
        position: absolute;
        left: 5rem;
        top: 3rem;
    }

    .graph {
        position: absolute;
        top: 5rem;
        right: 10rem;
    }

</style>