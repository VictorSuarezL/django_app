# %%
import pandas as pd
import json

# Carga el diccionario de renombramiento desde el archivo JSON
with open('column_dict.json', 'r') as f:
    nuevos_nombres = json.load(f)

df = pd.read_excel("../Principal.xlsx").drop_duplicates()

df = df.rename(columns=nuevos_nombres)

