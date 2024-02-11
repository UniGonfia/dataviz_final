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

    svg.append("text")
        .attr("x", -230)
        .attr("y", -50)
        .style("transform", 'rotate(-90deg)')
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .attr("fill", "white")
        .text("Number of events");


    // Assicurati che la selezione e l'append dei rettangoli siano corretti
    svg.append("g")
        .selectAll("g")
        // Entra nel dato stacked
        .data(stackedData)
        .enter().append("g")
        .attr("fill", d => color(d.key))
        .selectAll("rect")
        // Entra nei dati del singolo gruppo
        .data(d => d)
        .enter().append("rect")
            .attr("x", d => x(d.data.TIME_PERIOD))
            .attr("y", d => y(d[1]))
            .attr("height", d => y(d[0]) - y(d[1]))
            .attr("width", x.bandwidth())
            .on("mouseover", function(event, d) {
                // Mostra il tooltip
                tooltip.style("opacity", .9)
                    .html(`<strong>Year:</strong> ${d.data.TIME_PERIOD}<br/>
                            <strong>Type:</strong> ${d3.select(this.parentNode).datum().key}<br/>
                            <strong>Number of events:</strong> ${d[1] - d[0]}`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", function() {
                // Nascondi il tooltip
                tooltip.style("opacity", 0);
            });
    // Description
    document.querySelector('.description p').innerHTML = 
        `
        <strong> In this stacked bar chart, we can observe the quantity of disastrous events or those that generally caused discomfort in Europe. </strong> <br/>
        It's particularly interesting to note a peak in storms in 1990, attributed to various cyclones and tempests that primarily targeted 
        Northern Europe during that period. However, setting aside this localized phenomenon, it's crucial to recognize the overall increase 
        in such events, especially storms, extreme temperatures, and floods that have specifically affected the Eurozone.
        <br/><br/>
        The concerning aspect is that this trend is on the rise, which is undoubtedly linked to global warming, as supported by various studies.
        <br/><br/>
        This visualization underscores the growing impact of climate change on Europe, highlighting an upward trend in weather-related disasters. 
        The increased frequency and severity of these events call for urgent attention and action to mitigate the effects of global warming and protect 
        vulnerable regions. It serves as a stark reminder of the tangible consequences of climate change, emphasizing the need for continued research 
        and policy efforts to address this global challenge.
        <br/><br/>
        It is possible to see the exact number of events for each year in more detail by mousing over them.
        `;

</script>

<style>


</style>