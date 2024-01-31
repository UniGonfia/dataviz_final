import pandas as pd
import json

# Funzione per estrarre solamente la parte finale del nome della fonte dall'indicatore
def extract_final_part_of_source(indicator):
    # Prende solo l'ultima parte dopo l'ultimo punto
    return indicator.split(':')[-1].strip()

file_path = '../dataset/change_in_mean_sea_level.csv'  # Sostituisci con il percorso del tuo file CSV
sea_level_data = pd.read_csv(file_path)

sea_level_data['Date'] = sea_level_data['Date'].str.replace('D', '')
sea_level_data['Date'] = pd.to_datetime(sea_level_data['Date'], format='%m/%d/%Y')
sea_level_data['Year'] = sea_level_data['Date'].dt.year

european_seas = ['Baltic Sea', 'Mediterranean', 'North Sea', 'Adriatic Sea']
european_sea_level_data = sea_level_data[sea_level_data['Measure'].isin(european_seas)]

european_sea_level_data['Final_Source'] = european_sea_level_data['Indicator'].apply(extract_final_part_of_source)

grouped_european_sea_level_data = european_sea_level_data.groupby(['Measure', 'Year', 'Final_Source']).agg({'Value': 'mean'}).reset_index()

european_json_structure = {}
for _, row in grouped_european_sea_level_data.iterrows():
    sea = row['Measure']
    year = int(row['Year'])
    source = row['Final_Source']
    value = row['Value']

    if sea not in european_json_structure:
        european_json_structure[sea] = {}
    if year not in european_json_structure[sea]:
        european_json_structure[sea][year] = {}
    european_json_structure[sea][year][source] = value

json_data = json.dumps(european_json_structure, indent=4)

output_file_path = '../src/lib/data/change_in_level_by_sea.json'  
with open(output_file_path, 'w') as file:
    file.write(json_data)
