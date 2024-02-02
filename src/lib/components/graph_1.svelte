<script>
    import * as d3 from 'd3';
    import data from '$lib/data/air_emission_by_sectors.json';

    /*
        Data is like:
        "Agricolture, forestry and fishing": [
        {
            "TIME_PERIOD": "2010-Q1",
            "OBS_VALUE": 117442.351
        },
        {
            "TIME_PERIOD": "2010-Q2",
            "OBS_VALUE": 120182.728
        },
        {
            "TIME_PERIOD": "2010-Q3",
            "OBS_VALUE": 121224.023
        },
        ...
    */

    // Transform the data into a suitable format
    const dataset = Object.entries(data).map(([key, values]) => {
        return values.map(d => {
            return { 
                TIME_PERIOD: d3.timeParse("%Y-Q%q")(d.TIME_PERIOD), 
                key: key, 
                OBS_VALUE: +d.OBS_VALUE
            };
        });
    }).flat();

    // Group the data by TIME_PERIOD
    const sumstat = d3.group(dataset, d => d.TIME_PERIOD);

    // Stack the data
    const keys = Array.from(new Set(dataset.map(d => d.key)));
    const stackedData = d3.stack()
        .keys(keys)
        .value(([, values], key) => {
            const val = values.find(v => v.key === key);
            return val ? val.OBS_VALUE : 0;
        })(sumstat);

    // set the dimensions and margins of the graph
    const margin = { top: 40, right: 100, bottom: 130, left: 150 };
    const width = document.querySelector("svg").getBoundingClientRect().width - margin.left - margin.right;
    const height = document.querySelector("svg").getBoundingClientRect().height - margin.top - margin.bottom;

    // append the svg object to the body of the page
    const svg = d3.select("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Add X axis
    const x = d3.scaleTime()
        .domain(d3.extent(dataset, d => d.TIME_PERIOD))
        .range([0, width]);
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    // Add Y axis
    const y = d3.scaleLinear()
        .domain([0, d3.max(stackedData, d => d3.max(d, d => d[1]))])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // color palette
    const color = d3.scaleOrdinal()
        .domain(keys)
        .range(d3.schemeTableau10);

    // Show the areas
    svg.selectAll("mylayers")
        .data(stackedData)
        .join("path")
        .style("fill", d => color(d.key))
        .attr("d", d3.area()
            .x(d => x(d.data[0]))
            .y0(d => y(d[0]))
            .y1(d => y(d[1]))
        );

    

    // Create the area generator for the lines
    const lineGenerator = d3.area()
        .x(d => x(d.data[0]))
        .y0(d => y(d[0]))
        .y1(d => y(d[0])); // use d[0] for both y0 and y1 to make a line

    // Show the areas
    svg.selectAll("mylayers")
        .data(stackedData)
        .enter()
        .append("path")
        .style("fill", d => color(d.key))
        .attr("d", d3.area()
            .x(d => x(d.data[0]))
            .y0(d => y(d[0]))
            .y1(d => y(d[1]))
        );

    // Add the lines on top of the areas
    svg.selectAll("mylines")
        .data(stackedData)
        .enter()
        .append("path")
        .style("fill", "none")
        .style("stroke", "black")
        .style("stroke-width", 1)
        .attr("d", lineGenerator);

        // Add legend under the graph
    const legend = svg.append("g")
        .attr("transform", `translate(0,${height + 50})`)
        .selectAll("g")
        .data(keys)
        .join("g")
        .attr("transform", (d, i) => { // Adjust these values as needed to fit your layout
            const xSpacing = 235; // Horizontal spacing between legend items
            const ySpacing = 20;  // Vertical spacing between legend items

            const col = i % 3;    // Column index (0, 1, or 2)
            const row = Math.floor(i / 3); // Row index

            const xPosition = col * xSpacing;
            const yPosition = row * ySpacing;

            return `translate(${xPosition}, ${yPosition})`;
        });;

    legend.append("rect")
        .attr("width", 16)
        .attr("height", 16)
        .attr("fill", color);
    
    legend.append("text")
        .attr("x", 24)
        .attr("y", 9.5)
        .attr("dy", "0.35em")
        .attr("fill", "white")
        .style("font-size", "0.8em")
        .text(d => d);
    
    // Add text of unit in y axis
    svg.append("text")
        .attr("x", margin.left - 370)
        .attr("y", -110)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("transform", "rotate(-90deg)")
        .attr("fill", "white")
        .text("Tones");

    //Description
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


