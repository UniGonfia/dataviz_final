<script>
    import polarbear from '$lib/images/PolarBear.png';
    import polarbear_stand from '$lib/images/PolarBear_stand.png';
    import anime from 'animejs/lib/anime.es.js';
    import { onMount } from 'svelte';
    import Graph1 from '$lib/components/graph_1.svelte';
    import Graph2 from '$lib/components/graph_2.svelte';
    import Graph3 from '$lib/components/graph_3.svelte'
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

    function clean_graph() {
        const graph = document.querySelector('svg');
        graph.innerHTML = '';
        d3.select(graph).selectAll('*').remove();
    }
    
    let rendered = false;
    onMount(() => {
        rendered = true;
        animation_init();
        onscroll_animation();
        clean_graph();
        new Graph3({
            target: document.querySelector('body'),
        });
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

    <svg> </svg>

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
        font-size: 18px;
        width: 25rem;
        position: absolute;
        left: 5rem;
        top: 3rem;
    }

    svg {
        position: absolute;
        top: 2rem;
        right: 0;
        z-index: 100;
        display: block;
        margin-inline: auto;
        width: 60%;
        height: 40rem;
    }   

</style>