
import pandas as pd
import json

# Leggi i dati dal file CSV
file_path = '../dataset/countries_contributions.csv'  # Sostituisci con il percorso corretto del file
data = pd.read_csv(file_path)

# Selezioniamo solo le colonne necessarie
data = data[['geo', 'TIME_PERIOD', 'OBS_VALUE']]

# Creazione di un JSON del tipo: {country: {year: total_value}}
# Raggruppa i dati per paese e anno e calcola la somma dei valori
grouped_data = data.groupby(['geo', 'TIME_PERIOD']).sum()

# Converti il raggruppamento in un formato desiderato: {country: {year: total_value}}
final_structure = {}
for (country, year), row in grouped_data.iterrows():
    if country not in final_structure:
        final_structure[country] = {}
    final_structure[country][year] = row['OBS_VALUE']

# Scrivi i dati in un file JSON
with open('../src/lib/data/countries_contributions.json', 'w') as file:
    file.write(json.dumps(final_structure, indent=4))