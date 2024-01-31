<script>
    import * as d3 from 'd3';
    import iceMassData from '$lib/data/ice_mass_data.json';

    const margin = { top: 30, right: 80, bottom: 50, left: 80 };
    const width = document.querySelector("svg").getBoundingClientRect().width - margin.left - margin.right;
    const height = (document.querySelector("svg").getBoundingClientRect().height/2 - margin.top - margin.bottom);
    
    const glaciers = ['greenland', 'antarctica'];

    glaciers.forEach((glacier, index) => {
        // Prepara i dati
        const data = iceMassData[glacier].map(d => ({ year: d[0], mass: d[1], uncertainty: d[2] }));
        
        // Crea il container SVG
        const svg = d3.select('#graph').append("svg")
            .attr("width", (width + margin.left + margin.right))
            .attr("height", (height + margin.top + margin.bottom))
            .attr("transform", `translate(${0},${(height + margin.top + margin.bottom) * index + 30} )`);

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
            .attr("x", 150)             
            .attr("y", (220))
            .attr("text-anchor", "middle")  
            .style("font-size", "16px") 
            .attr("fill", "white")
            .style("text-decoration", "underline")  
            .text(glacier.toUpperCase());

    });


    document.querySelector('.description p').innerHTML = 
        `
        The graph shows the CO2 emissions of European countries divided by sector. 
        <br/> <br/>
        As we can see from the graph, the sector that contributes most to pollution in Europe is the manufacturing sector and the energy sector. 
        <br/>
        Focusing mainly on these sectors and reducing emissions would certainly lead to a lowering of pollution in Europe, and it is very interesting to note 
        the lowering of emissions around 2020, probably caused by the first quarantines for covid, causing a stop in the manufacturing industry and a consequent 
        lowering of the use of energy resources.
        <br/> <br/>
        According to a recent EEA analysis, using the best available techniques and implementing the more ambitious targets of the Industrial Emissions Directive 
        would result in substantial emission reductions: 91 % for sulphur dioxide, 82 % for particulate matter and 79 % for nitrogen oxides.
        <br/> <br/>
        Looking at the graph, we can also see that we have a slight downward trend in the maufacturing and energy sectors, which encourages us and might make us 
        think that the standards are succeeding at least to a small extent.
        `;


</script>