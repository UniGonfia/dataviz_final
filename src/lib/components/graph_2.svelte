<script>
    import * as d3 from 'd3';
    import data_file from '$lib/data/air_emission_by_sector_and_country.json';

    /*
        data_file is like:
        {"AT": {"Agricolture, forestry and fishing": [{"2010": 178400.42}, {"2011": 176638.22}, {"2012": 175721.78} ...
    */

    // set the dimensions and margins of the graph
    const margin = { top: 0, right: 0, bottom: 0, left: 0 };
    const width = document.querySelector("svg").getBoundingClientRect().width - margin.left - margin.right;
    const height = document.querySelector("svg").getBoundingClientRect().height - margin.top - margin.bottom;

    // Definisci le proiezioni per le diverse parti dell'Europa
    const europeMain = d3.geoMercator()
        .center([15, 50]) // Centro sull'Europa centrale
        .scale(800)
        .translate([width / 2, height / 2]);

    let scale = 800;
    if (width < 1100) {
        scale = 600;
    }

    if (width < 900) {
        scale = 500;
    }

    const scandinavia = d3.geoMercator()
        .center([36, 69]) // Centro sulla Scandinavia
        .scale(scale)
        .translate([width, height / 5]); // Modifica per ottimizzare la posizione

    // Funzione per selezionare la proiezione in base al paese
    function getProjection(feature) {
        const iso = feature.id; // Assicurati che 'id' corrisponda al campo giusto nel tuo GeoJSON
        if (iso === 'SWE' || iso === 'FIN') {
        return scandinavia;
        }
        return europeMain;
    }

    // Function to aggregate emissions data
    function aggregateEmissions(year) {
        const emissionsByCountry = {};
        Object.entries(data_file).forEach(([countryCode, sectors]) => {
            let totalEmissions = 0;
            Object.values(sectors).forEach(sector => {
                sector.forEach(yearData => {
                    if (yearData[year]) {
                        totalEmissions += yearData[year];
                    }
                });
            });
            emissionsByCountry[countryCode] = totalEmissions;
        });
        return emissionsByCountry;
    }

    // Color scale
    const colorScale = d3
            .scaleSequential(d3.interpolateYlOrRd)
            .domain([0, 1500000000])
            .nice();



    // append the svg object to the body of the page
    const svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

    // Load external data and boot
    d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson").then(function(data) {

        // Filter data to include only European countries based on the countryCodes mapping
        data.features = data.features.filter(d => countryCodes[d.id] !== undefined);

        // Draw the map with initial year's data
        const paths = svg.append("g")
            .selectAll("path")
            .data(data.features)
            .join("path")
            .attr("fill", d => {
                const emissions = aggregateEmissions(document.getElementById("yearSlider").value)[countryCodes[d.id]];
                return colorScale(emissions);
            })
            .attr("d", d => d3.geoPath().projection(getProjection(d))(d))
            .style("stroke", "none");

        const tooltip = d3.select("#tooltip");

        // Update the map based on the selected year
        document.getElementById("yearSlider").addEventListener("input", function() {
            const selectedYear = this.value;
            document.getElementById("selectedYear").textContent = selectedYear;
            const emissionsByCountry = aggregateEmissions(selectedYear);
            paths.attr("fill", d => {
                const emissions = emissionsByCountry[countryCodes[d.id]];
                return colorScale(emissions);
            });


            // Modify the paths to include mouse events for the tooltip
            paths
                .on("mouseover", function(event, d) {
                    tooltip.transition().duration(200).style("opacity", 1); // Show the tooltip
                    const countryCode = countryCodes[d.id];
                    const sectors = data_file[countryCode];
                    let tooltipHtml = `<strong>${d.properties.name}</strong><br/>`; // Use the country name from the GeoJSON properties if available
                    Object.entries(sectors).forEach(([sector, data]) => {
                        const yearData = data.find(yearData => yearData[document.getElementById("yearSlider").value]);
                        const emissions = yearData ? yearData[document.getElementById("yearSlider").value] : "Data not available";
                        tooltipHtml += `${sector}: ${emissions.toFixed(2)}<br/>`; // Format numbers as needed
                    });
                    tooltip.html(tooltipHtml)
                        .style("left", (event.pageX + 15) + "px") // Position the tooltip
                        .style("top", (event.pageY - 28) + "px");
                })
                .on("mouseout", function() {
                    tooltip.transition().duration(500).style("opacity", 0); // Hide the tooltip
            });
        });


        // Modify the paths to include mouse events for the tooltip
        paths
            .on("mouseover", function(event, d) {
                tooltip.transition().duration(200).style("opacity", 1); // Show the tooltip
                const countryCode = countryCodes[d.id];
                const sectors = data_file[countryCode];
                let tooltipHtml = `<strong>${d.properties.name}</strong><br/>`; // Use the country name from the GeoJSON properties if available
                Object.entries(sectors).forEach(([sector, data]) => {
                    const yearData = data.find(yearData => yearData[document.getElementById("yearSlider").value]);
                    const emissions = yearData ? yearData[document.getElementById("yearSlider").value] : "Data not available";
                    tooltipHtml += `${sector}: ${emissions.toFixed(2)}<br/>`; // Format numbers as needed
                });
                tooltip.html(tooltipHtml)
                    .style("left", (event.pageX + 15) + "px") // Position the tooltip
                    .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", function() {
                tooltip.transition().duration(500).style("opacity", 0); // Hide the tooltip
        });
    });


    const countryCodes = {
        AUT: 'AT', // Austria
        BEL: 'BE', // Belgium
        BGR: 'BG', // Bulgaria
        CYP: 'CY', // Cyprus
        CZE: 'CZ', // Czech Republic
        DEU: 'DE', // Germany
        DNK: 'DK', // Denmark
        EST: 'EE', // Estonia
        ESP: 'ES', // Spain
        FIN: 'FI', // Finland
        FRA: 'FR', // France
        GRC: 'EL', // Greece
        HRV: 'HR', // Croatia
        HUN: 'HU', // Hungary
        IRL: 'IE', // Ireland
        ITA: 'IT', // Italy
        LTU: 'LT', // Lithuania
        LUX: 'LU', // Luxembourg
        LVA: 'LV', // Latvia
        MLT: 'MT', // Malta
        NLD: 'NL', // Netherlands
        POL: 'PL', // Poland
        PRT: 'PT', // Portugal
        ROU: 'RO', // Romania
        SWE: 'SE', // Sweden
        SVN: 'SI', // Slovenia
        SVK: 'SK', // Slovakia
    };

    //Add legend
    const legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${100},${100})`)
        .selectAll("g")
        .data(colorScale.ticks(10).slice(1).reverse())
        .join("g");

    legend.append("rect")
        .attr("x", (d, i) => i * 40)
        .attr("y", -50)
        .attr("width", 100)
        .attr("height", 10)
        .attr("fill", colorScale);


    legend.append("text")
        .attr("x", (d, i) => i * 50)
        .attr("y", -60)
        .attr("dy", "0.35em")
        .attr("fill", "white")
        .style("font-size", "0.8em")
        .text(d => d3.format(".2s")(d).replace("G", "Kt").replace("M", "Mt").replace("k", "t"));

    //Add + int he first text
    legend.append("text")
        .attr("x", -10)
        .attr("y", -60)
        .attr("dy", "0.30em")
        .attr("fill", "white")
        .style("font-size", "0.5em")
        .text("+");


     //Description
     document.querySelector('.description p').innerHTML = 
        `
        This map highlights the major producers of CO2 emissions over the years. Interestingly, when comparing the current data to that of 2010, there's a noticeable decrease in emissions, particularly from the two main contributors: Germany and France. This trend aligns with previous data and underscores the progress made, though it's crucial to acknowledge that the journey towards zero emissions is far from over.
        <br/><br/>
        Both countries have expressed a strong commitment to further reducing their carbon footprint. By 2030, they aim to cut emissions by 40% compared to current levels. This ambitious goal is partly achievable through shifts in energy production strategies. France, for example, plans to increasingly rely on nuclear energy, while Germany has set a target to reach zero emissions by 2045, mainly reducing greenhouse emissions, and focusing mainly on renewable energies.
        <br/><br/>
        These developments indicate a positive direction in the fight against climate change, highlighting the efforts and strategies of countries leading in emission reductions.
        <br/><br/>
        It is possible to see the sectors and their emissions for each country in more detail by mousing over them.
        `;


</script>


<div class="input_range">
    <label for="yearSlider">Select Year:</label>
    <input type="range" id="yearSlider" name="yearSlider"
        min="2010" max="2022" value="2022" step="1">
    <p>Year: <span id="selectedYear">2022</span></p>
</div>


<style>

    .input_range {
        position: absolute;
        display: flex;
        flex-direction: column;
        text-align: center;
        background-color: transparent;
        bottom: 8rem;
        right: 15%;
        padding: 10px;
        width: 30rem;
        color: white;
        z-index: 200;
        accent-color: white;
    }



</style>