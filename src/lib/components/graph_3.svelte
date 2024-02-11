<script>
    import * as d3 from 'd3';
    import data_file from '$lib/data/countries_contributions.json';

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
    function aggregateContributions(year) {
        const contributionsByCountry = {};
        Object.entries(data_file).forEach(([countryCode, yearsData]) => {
            const totalContributions = yearsData[year] || 0;
            contributionsByCountry[countryCode] = totalContributions;
        });
        return contributionsByCountry;
    }

    // Scala dei colori (aggiustare il dominio in base ai tuoi dati)
    const colorScale = d3
            .scaleSequential(d3.interpolateYlOrRd)
            .domain([0, 5000])
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
                const emissions = aggregateContributions(document.getElementById("yearSlider").value)[countryCodes[d.id]];
                return colorScale(emissions);
            })
            .attr("d", d => d3.geoPath().projection(getProjection(d))(d))
            .style("stroke", "none");

        // Aggiungi il tooltip
        const tooltip = d3.select("#tooltip");


        // Update the map based on the selected year
        document.getElementById("yearSlider").addEventListener("input", function() {
            const selectedYear = this.value;
            document.getElementById("selectedYear").textContent = selectedYear;
            const emissionsByCountry = aggregateContributions(selectedYear);
            paths.attr("fill", d => {
                const emissions = emissionsByCountry[countryCodes[d.id]];
                return colorScale(emissions);
            });



            // Modifica i path per includere gli eventi del mouse per il tooltip
            paths.on("mouseover", function(event, d) {
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", 1);
                    const countryCode = countryCodes[d.id];
                    const year = document.getElementById("yearSlider").value;
                    const contributions = data_file[countryCode] ? (data_file[countryCode][year] || 0) : 0;
                    tooltip.html(`<strong>Country:</strong> ${d.properties.name}<br/>
                                <strong>Year:</strong> ${year}<br/>
                                <strong>Contributions:</strong> ${contributions}`)
                        .style("left", (event.pageX) + "px")
                        .style("top", (event.pageY - 28) + "px");
                })
                .on("mouseout", function(event, d) {
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                });


        });



        // Modifica i path per includere gli eventi del mouse per il tooltip
        paths.on("mouseover", function(event, d) {
            tooltip.transition()
                .duration(200)
                .style("opacity", 1);
            const countryCode = countryCodes[d.id];
            const year = document.getElementById("yearSlider").value;
            const contributions = data_file[countryCode] ? (data_file[countryCode][year] || 0) : 0;
            tooltip.html(`<strong>Country:</strong> ${d.properties.name}<br/>
                        <strong>Year:</strong> ${year}<br/>
                        <strong>Contributions:</strong> ${contributions}`)
                .style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout", function(event, d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
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
        .attr("x", (d, i) => i * 30)
        .attr("y", -50)
        .attr("width", 100)
        .attr("height", 10)
        .attr("fill", colorScale);


    legend.append("text")
        .attr("x", (d, i) => i * 40)
        .attr("y", -60)
        .attr("dy", "0.35em")
        .attr("fill", "white")
        .style("font-size", "0.8em")
        .text(d => d3.format(".2s")(d).replace("k", "B"));

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
        <strong> This map provides an overview of the financial contributions made by various countries towards the global $100 billion 
        commitment for climate finance under the United Nations Framework Convention on Climate Change (UNFCCC). <strong/> <br/> It's noteworthy 
        that the countries historically responsible for the highest carbon dioxide emissions, such as France and Germany, are among 
        the top contributors to this cause.
        Over time, we observe an encouraging trend: contributions from all participating nations have generally increased, highlighting a 
        collective effort to address climate challenges more effectively.
        <br/><br/>
        Moreover, this financial contribution is an important metric within the European Union's Sustainable Development Goals (SDG) indicator set, 
        particularly for monitoring progress towards SDG 13, which focuses on climate action. This alignment underscores the importance the 
        European Commission places on environmental sustainability, as part of its broader European Green Deal priorities. The Deal aims to 
        make Europe the first climate-neutral continent by 2050, demonstrating a commitment to environmental stewardship, economic growth, 
        and social inclusion.
        <br/><br/>
        It is possible to see the exact contribution for each country in more detail by mousing over them.
        `;


</script>


<div class="input_range">
    <label for="yearSlider">Select Year:</label>
    <input type="range" id="yearSlider" name="yearSlider"
        min="2014" max="2022" value="2022" step="1">
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


    @media screen and (max-width: 1400px) {
        .input_range {
            bottom: 3rem;
        }
    }

    @media screen and (max-height: 700px) {
        .input_range {
            bottom: 3rem;
            width: 15rem;
            right: 2rem;
        }
    }

</style>