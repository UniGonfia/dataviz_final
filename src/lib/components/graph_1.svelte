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
    const margin = { top: 30, right: 100, bottom: 30, left: 100 };
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
</script>


