<script>
    import * as d3 from 'd3';
    import rawData from '$lib/data/change_in_level_by_sea.json';

    let data = [];
    Object.keys(rawData).forEach(sea => {
        Object.entries(rawData[sea]).forEach(([year, resources]) => {
        Object.entries(resources).forEach(([resource, value]) => {
            if (resource == 'Trend') return;
            data.push({ sea, year: +year, resource, value });
        });
        });
    });
    
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // Set dimensions and margins
    const margin = { top: 20, right: 100, bottom: 60, left: 50 };
    const width = document.querySelector("svg").getBoundingClientRect().width - margin.left - margin.right;
    const height = (document.querySelector("svg").getBoundingClientRect().height/3 - margin.top - margin.bottom);
    // Creare un SVG per ogni mare
    const seas = ['Adriatic Sea', 'Baltic Sea', 'Mediterranean'];
    seas.forEach((sea, index) => {
        // Filtrare i dati per il mare corrente
        const seaData = data.filter(d => d.sea === sea);
    
        // Creare il container SVG
        const svg = d3.select('#graph').append("svg")
            .attr("width", (width + margin.left + margin.right))
            .attr("height", (height + margin.top + margin.bottom))
            .attr("transform", `translate(${0},${(height + margin.top + margin.bottom) * index + 20} )`);

        const years = seaData.map(d => d.year);

        // Imposta il dominio dell'asse x con tutti gli anni (assicurati che siano unici)
        const uniqueYears = [...new Set(years)]; // Rimuove eventuali duplicati
        const x = d3.scaleBand()
            .domain(uniqueYears)
            .range([0, width])
            .padding([0.2]);

        // Calcola gli anni da mostrare come etichette (ad esempio, ogni 10 anni)
        const tickInterval = 3;
        const tickValues = uniqueYears.filter((year, i) => i % tickInterval === 0);

        svg.append("g")
            .attr("transform", `translate(${margin.left},${height})`)
            .call(d3.axisBottom(x).tickValues(tickValues).tickSizeOuter(0));

    
        const y = d3.scaleLinear()
            .domain([d3.min(seaData, d => d.value), d3.max(seaData, d => d.value)])
            .range([height, 0]);

    
        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y));


        // Color scale
    
        // Line generator
        const line = d3.line()
            .x(d => x(d.year))
            .y(d => y(d.value));
    
        // Group data by resource for this sea
        const resources = d3.groups(seaData, d => d.resource);

        // Draw lines for each resource
        resources.forEach(([resource, values]) => {
            svg.append("path")
                .datum(values)
                .attr("fill", "none")
                .attr("stroke", color(resource))
                .attr("stroke-width", 1.5)
                .attr("transform", `translate(${margin.left},0)`)
                .attr("d", line);
            });

        // Add title
        svg.append("text")
        .attr("x", 150)             
        .attr("y", (20))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .attr("fill", "white")
        .style("text-decoration", "underline")  
        .text(sea);

        if (index == 2) {
            //add legend
            const legend = svg.append("g")
                .attr("transform", `translate(${margin.left},${height + 15})`);

            legend.selectAll("rect")
                .data(resources.map(d => d[0]))
                .join("rect")
                .attr("x", (d, i) => i * 200)
                .attr("y", (d, i) => 25)
                .attr("width", 10)
                .attr("height", 10)
                .attr("fill", d => color(d));

            legend.selectAll("text")
                .data(resources.map(d => d[0]))
                .join("text")
                .attr("x", (d, i) => i * 200 + 15)
                .attr("y", (d, i) => 35)
                .text(d => d)
                .attr("text-anchor", "start")
                .style("alignment-baseline", "middle")
                .attr("fill", "white");
        }



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

    // ... (Description code)
</script>
