<script>
    import * as d3 from 'd3';
    import iceMassData from '$lib/data/ice_mass_data.json';

    const margin = { top: 30, right: 80, bottom: 50, left: 100 };
    const width = document.querySelector("svg").getBoundingClientRect().width - margin.left - margin.right;
    const height =  document.querySelector("svg").getBoundingClientRect().height/2 - margin.top - margin.bottom + 20;
    
    const glaciers = ['greenland', 'antarctica'];

    glaciers.forEach((glacier, index) => {
        // Prepara i dati
        const data = iceMassData[glacier].map(d => ({ year: d[0], mass: d[1], uncertainty: d[2] }));
        
        // Crea il container SVG
        const svg = d3.select('#graph').append("svg")
            .attr("width", (width + margin.left + margin.right))
            .attr("height", (height + margin.top + margin.bottom))
            .attr("x", `0`)
            .attr("y", `${index * height + 80 * index}`)

        // Imposta il dominio dell'asse x con tutti gli anni (assicurati che siano unici)
        const years = data.map(d => d.year);
        const uniqueYears = [...new Set(years)]; // Rimuove eventuali duplicati
        const x = d3.scaleBand()
            .domain(uniqueYears)
            .range([0, width])
            .padding([0.2]);

        // Calcola gli anni da mostrare come etichette (ad esempio, ogni 10 anni)
        const tickInterval = 20;
        const tickValues = uniqueYears.filter((year, i) => i % tickInterval === 0);

        svg.append("g")
            .attr("transform", `translate(${margin.left},${height})`)
            .call(d3.axisBottom(x).tickValues(tickValues).tickSizeOuter(0))
            .selectAll("text")
            .text(d => `${d.toString().split(".")[0]}`); // Rimuove il primo numero dell'anno
        
        // Imposta il dominio dell'asse y
        const y = d3.scaleLinear()
            .domain([d3.min(data, d => d.mass), d3.max(data, d => d.mass)])
            .range([height, 0]);
        
        // Aggiungi l'asse y
        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y));

        // Aggiungi la linea
        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "white")
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
                .x(d => x(d.year) + margin.left + x.bandwidth() / 2)
                .y(d => y(d.mass))
            );
        
        // Add title
        svg.append("text")
            .attr("x", 160)             
            .attr("y", (215))
            .attr("text-anchor", "middle")  
            .style("font-size", "16px") 
            .attr("fill", "white")
            .style("text-decoration", "underline")  
            .text(glacier.toUpperCase());
            

        svg.append("text")
            .attr("x", -100)             
            .attr("y", (20))
            .style("transform", 'rotate(-90deg)')
            .attr("text-anchor", "middle")  
            .style("font-size", "16px") 
            .attr("fill", "white")
            .text("Gt of ice");
    });


    document.querySelector('.description p').innerHTML = 
        `
        <strong> To conclude, this chart illustrates the melting of glaciers in Antarctica and Greenland. <strong/> <br/> Connected to the previous charts, it continues to demonstrate the negative effects of climate change on our planet Earth, and it's alarming how rapidly the ice is melting.
        <br/><br/>
        According to signals and observations collected by satellites, the melting of the two largest Antarctic glaciers, Pine Island and Thwaites, has reached the point of no return. This could lead to a sea-level rise of more than 3 meters. 
        <br/><br/>
        According to a study published in PNAS, the massive loss of ice recorded in Greenland over the last 20 years is due to the process of "undercutting." This occurs when the glaciers, retreating, come into contact with the warmer water masses underneath. The ice is then melted from below, leading to greater thinning, which promotes further retreat.
        <br/><br/>
        This melting is also causing changes in the habitat of many marine and terrestrial species. If the characteristics of the habitat that hosts certain animal species change, those species, unable to adapt, risk extinction, such as the polar bears.
        `

</script>