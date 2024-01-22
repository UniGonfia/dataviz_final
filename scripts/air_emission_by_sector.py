import pandas as pd
import json
# Read the data from the CSV file
data = pd.read_csv('../dataset/air_emission_by_sector.csv', sep=',')

# Map the column nace_r2 with the full name
def map_type(nace_r2):
    match nace_r2:
        case 'A':
            return 'Agricolture, forestry, fishing'
        case 'B':
            return 'Mining and quarryng'
        case 'C':
            return 'Manufacturing'
        case 'D':
            return 'Electricity, gas, steam'
        case 'E':
            return 'Water supply'
        case 'F':
            return 'Construction'
        case 'G-U_X_H':
            return 'Services'
        case 'H':
            return 'Transportation and storage'
        case 'HH':
            return 'All NACE activities'
        case 'TOTAL_HH':
            return 'Total by household'

data = data.assign(type=data['nace_r2'].map(map_type))

# Create a .json with the type of activity together with the quarterly in column TIME_PERIOD, and the value in OBS_VALUE
data = data[['type', 'TIME_PERIOD', 'OBS_VALUE']]

# Create a .json like that: {type: [TIME_PERIOD: OBS_VALUE]}
# Group by type and create the desired JSON structure
data = data.groupby('type').apply(lambda x: x[['TIME_PERIOD', 'OBS_VALUE']].to_dict('records')).to_dict()

# Write the data in a .json file
with open('../src/lib/data/air_emission_by_sectors.json', 'w') as file:
    file.write(json.dumps(data, indent=2))

