import pandas as pd

# Read the data from the CSV file
data = pd.read_csv('../dataset/air_emission.csv', sep=',')

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
data[['type', 'TIME_PERIOD', 'OBS_VALUE']].to_json('../dataset/air_emission.json', orient='records')

print(data[['nace_r2', 'type']])