import pandas as pd
import json

def extract_disaster_category(indicator):
    return indicator.split(": ")[-1].strip()

climate_disasters_file_path = '../dataset/climate_disaster_frequency.csv' 

climate_data = pd.read_csv(climate_disasters_file_path)

european_countries_iso3 = [
    "ALB", "AND", "ARM", "AUT", "AZE", "BLR", "BEL", "BIH", "BGR", "HRV", "CYP", 
    "CZE", "DNK", "EST", "FIN", "FRA", "GEO", "DEU", "GRC", "HUN", "ISL", "IRL", 
    "ITA", "KAZ", "XKX", "LVA", "LIE", "LTU", "LUX", "MLT", "MDA", "MCO", "MNE", 
    "NLD", "MKD", "NOR", "POL", "PRT", "ROU", "RUS", "SMR", "SRB", "SVK", "SVN", 
    "ESP", "SWE", "CHE", "TUR", "UKR", "GBR", "VAT"
]

european_data = climate_data[climate_data['ISO3'].isin(european_countries_iso3)]

years = [f"F{year}" for year in range(1980, 2023)]

grouped_data = {}
for index, row in european_data.iterrows():
    country = row['ISO3']
    if country not in grouped_data:
        grouped_data[country] = {}

    for year in years:
        if pd.notna(row[year]):
            year_short = int(year[1:])  # Converte 'F1980' in 1980
            if year_short not in grouped_data[country]:
                grouped_data[country][year_short] = {}
            
            category = extract_disaster_category(row['Indicator'])
            if category not in grouped_data[country][year_short]:
                grouped_data[country][year_short][category] = 0
            grouped_data[country][year_short][category] += row[year]

json_data = json.dumps(grouped_data, indent=4)

output_json_path = '../src/lib/data/disasters_by_countries.json' 

with open(output_json_path, 'w') as file:
    file.write(json_data)
