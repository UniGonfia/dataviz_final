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
    const height = document.querySelector("svg").getBoundingClientRect().height/3 - margin.top - margin.bottom + 20;
    // Creare un SVG per ogni mare
    const seas = ['Adriatic Sea', 'Baltic Sea', 'Mediterranean'];
    seas.forEach((sea, index) => {
        // Filtrare i dati per il mare corrente
        const seaData = data.filter(d => d.sea === sea);
    
        // Creare il container SVG
        const svg = d3.select('#graph').append("svg")
            .attr("width", (width + margin.left + margin.right))
            .attr("height", (height + margin.top + margin.bottom))
            .attr("x", `0`)
            .attr("y", `${index * height + 40 * index}`)

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

        //Add mm at the end of the y axis
        svg.append("text")
            .attr("x", margin.left - 100)
            .attr("y", 10)
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("transform", "rotate(-90deg)")
            .attr("fill", "white")
            .text("mm");



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
        <strong> This chart is important for demonstrating the causes of climate change, such as sea-level rise. <strong/> <br/> In this instance, it showcases three European seas. 
        To construct this chart, four main data sources were combined to create a continuous measurement. 
        <br/>
        It's significant that since 1992, the sea level for all three has risen by at least 5 cm, and by as much as 15 cm for the Baltic Sea, marking a disastrous phenomenon. 
        This rise is attributed to 26% glacier melt, 15% to the melting of Greenland, but primarily, 46% is due to thermal expansion and the consequent 
        increase in temperatures. Some studies suggest that by 2200, if the current trends continue and if all remaining fossil fuels on Earth were 
        consumed, the sea could rise by as much as 60 meters.
        <br/><br/>
        When sea levels rise at the rate observed in recent years, even a small increase can have devastating effects on coastal and inland habitats: destructive erosion, flooding of wetlands, contamination of aquifers and agricultural lands with saltwater, and loss of habitat for fish, birds, and plants.
        And this ties back to the increase in disastrous events we've seen before, leading us further to demonstrate that climate change is not a hoax as some people believe, but a reality that is here and now.
        `;

    // ... (Description code)
</script>
