<script>
    import * as d3 from 'd3';
    import data from '$lib/data/disasters_by_years.json';

    const subgroups = ["Flood", "Storm", "Drought", "Extreme temperature", "Wildfire", "Landslide"];
    const groups = Object.keys(data);
    
    let dataset = [];
    for (const group of groups) {
        for (const subgroup of subgroups) {

            dataset.push({
                TIME_PERIOD: group,
                [subgroup]: data[group][subgroup]
            });
        }
    }


    // Stack the data
    const stackedData = d3.stack()
        .keys(subgroups)
        (dataset);

        
    // Set dimensions and margins
    const margin = { top: 40, right: 100, bottom: 100, left: 100 };
    const width = document.querySelector("svg").getBoundingClientRect().width - margin.left - margin.right;
    const height = document.querySelector("svg").getBoundingClientRect().height - margin.top - margin.bottom;

    // Append SVG object
    const svg = d3.select("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);



    // Imposta il dominio dell'asse x con tutti gli anni
    const x = d3.scaleBand()
        .domain(groups) // 'groups' dovrebbe essere l'elenco di tutti gli anni
        .range([0, width])
        .padding([0.2]);

    // Calcola gli anni da mostrare come etichette
    const tickInterval = 5; // Mostra un'etichetta ogni 5 anni
    const tickValues = groups.filter((_, i) => i % tickInterval === 0);

    // Aggiorna l'asse x con i tickValues selezionati
    svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).tickValues(tickValues).tickSizeOuter(0));

    const y = d3.scaleLinear()
        .domain([0, d3.max(stackedData, d => d3.max(d, d => d[1]))])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // Color palette
    const color = d3.scaleOrdinal()
        .domain(subgroups)
        .range(d3.schemeTableau10);

    svg.append("g")
        .selectAll("g")
        .data(stackedData)
        .join("g")
        .attr("fill", d => color(d.key))
        .selectAll("rect")
        .data(d => d)
        .join("rect")
            .attr("x", d => x(d.data.TIME_PERIOD))
            .attr("y", d => y(d[1]))
            .attr("height", d => y(d[0]) - y(d[1]))
            .attr("width",x.bandwidth())

    
    // Creare l'elemento tooltip
    const tooltip = d3.select("#tooltip");

    // Aggiungere eventi mouseover e mouseout alle barre
    svg.selectAll("rect")
        .on("mouseover", function(event, d) {
            tooltip.transition()
                .duration(200)
                .style("opacity", .9);
            tooltip.html(`<strong>Year:</strong> ${d.data.TIME_PERIOD}<br/>
                        <strong>Type:</strong> ${d3.select(this.parentNode).datum().key}<br/>
                        <strong>Number of events:</strong> ${d[1] - d[0]}`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout", function(d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        });

    const legend = svg.append("g")
        .attr("transform", `translate(${0}, ${height + 50})`);

    legend.selectAll("rect")
        .data(subgroups)
        .join("rect")
        .attr("x", (d, i) => i % 3 * 200)
        .attr("y", (d, i) => Math.floor(i / 3) * 20)
        .attr("width", 10)
        .attr("height", 10)
        .attr("fill", d => color(d))

    legend.selectAll("text")
        .data(subgroups)
        .join("text")
        .attr("x", (d, i) => i % 3 * 200 + 15)
        .attr("y", (d, i) => Math.floor(i / 3) * 20 + 10)
        .text(d => d)
        .attr("text-anchor", "start")
        .style("alignment-baseline", "middle")
        .attr("fill", "white")


    // Description
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

<div id="tooltip" class="tooltip"></div>

<style>

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
        z-index: 10000;
    }

</style>