import pandas as pd
import json
# Read the data from the CSV file
data = pd.read_csv('../dataset/air_emission_by_sector_and_country.csv', sep=',')

# Map the column nace_r2 with the full name
def map_type(nace_r2):
    match nace_r2:
        case 'A':
            return 'Agricolture, forestry and fishing'
        case 'B':
            return 'Mining and quarryng'
        case 'C':
            return 'Manufacturing'
        case 'D':
            return 'Electricity, gas, steam and air conditioning supply'
        case 'E':
            return 'Water supply; sewerage, waste management and remediation activities'
        case 'F':
            return 'Construction'
        case 'G-U_X_H':
            return 'Services (except transportation and storage)'
        case 'H':
            return 'Transportation and storage'
        case 'HH':
            return 'All NACE activities plus households'
        case 'TOTAL_HH':
            return 'Total activities by households'

data = data.assign(type=data['nace_r2'].map(map_type))

# Create a .json with the type of activity together with the quarterly in column TIME_PERIOD, and the value in OBS_VALUE
data = data[['geo', 'type', 'TIME_PERIOD', 'OBS_VALUE']]

# Create a .json like that: {country: {type: [TIME_PERIOD: OBS_VALUE]}}
# Grouping the data by country and type and creating the JSON structure
grouped_data = data.groupby(['geo', 'type']).apply(
    lambda x: [{row['TIME_PERIOD']: row['OBS_VALUE']} for _, row in x.iterrows()]
).to_dict()

# Converting the nested grouping into the desired format: {country: {type: [TIME_PERIOD: OBS_VALUE]}}
final_structure = {}
for (country, type_), values in grouped_data.items():
    if country not in final_structure:
        final_structure[country] = {}
    final_structure[country][type_] = values

# Write the data in a .json file
with open('../src/lib/data/air_emission_by_sector_and_country.json', 'w') as file:
    file.write(json.dumps(final_structure, indent=None))