import pandas as pd
from io import StringIO
import json

# Funzione per leggere i dati dal file, saltando le righe che iniziano con 'HDR'
def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data_lines = [line for line in lines if not line.startswith('HDR')]
    data_str = ''.join(data_lines)
    data = pd.read_csv(StringIO(data_str), delim_whitespace=True, header=None)
    return data

# Percorsi dei file
greenland_file_path = '../dataset/greenland.txt'  # Sostituisci con il percorso corretto
antarctica_file_path = '../dataset/antartica.txt' # Sostituisci con il percorso corretto

# Leggi i dati
greenland_data = read_data(greenland_file_path)
antarctica_data = read_data(antarctica_file_path)

# Crea un dizionario per memorizzare i dati
data_dict = {
    "greenland": greenland_data.values.tolist(),
    "antarctica": antarctica_data.values.tolist()
}

# Converti il dizionario in JSON
json_data = json.dumps(data_dict)

# Salva i dati JSON in un file
output_file_path = '../src/lib/data/ice_mass_data.json'  # Sostituisci con il percorso di output desiderato
with open(output_file_path, 'w') as file:
    file.write(json_data)

# Percorso del file di output
print("File JSON salvato in:", output_file_path)
