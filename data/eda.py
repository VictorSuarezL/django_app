import pandas as pd
import json

df = pd.read_excel("./data/Datos.xlsx", sheet_name="Export_datos")

# df

# # Get unique values for Marca variable in df without nan values
# unique_values = df['Tipo de IVA'].unique()
# unique_values = unique_values[~pd.isnull(unique_values)]

# print(unique_values)

# # Export unique values to a json file with name iva.json
# unique_values = unique_values.tolist()
# with open('data/iva.json', 'w') as f:
#     json.dump(unique_values, f)
    

def transform_data(df, col_to_read, name_json):
    unique_values = df[col_to_read].unique()
    unique_values = unique_values[~pd.isnull(unique_values)]
    unique_values = unique_values.tolist()
    print(unique_values)
    with open(f'data/{name_json}.json', 'w') as f:
        json.dump(unique_values, f)

transform_data(df, 'Tipo de IVA', 'iva')
transform_data(df, 'Servicio anterior', 'servicio_anterior')
transform_data(df, 'Garantía', 'garantia')


df