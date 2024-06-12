
import pandas as pd
import json
import os

# from catalog.models import Brand

# ------ Load data from excel to database ------

def date_parser(x):
    return pd.to_datetime(x, format="%d/%m/%y").date()


# Carga los datos del archivo Excel
df = pd.read_excel(
    "./data/Principal.xlsx",
    sheet_name="Principal",
    parse_dates=True,
    date_format=date_parser,
    engine='openpyxl'
)

with open("data/json/column_dict.json", "r") as f:
    nuevos_nombres = json.load(f)

df.rename(columns=nuevos_nombres, inplace=True)

# df = df.drop(df.index[5469])

def create_unique_values_json(df, column):
    json_dict = {}
    df[column] = df[column].astype(str)
    unique_values = sorted(df[column].unique().tolist())
    json_dict[column] = unique_values

    json_str = json.dumps(json_dict, ensure_ascii=False, indent=4)
    output_file = f"data/json/{column}.json"
    if not os.path.exists(output_file):
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(json_str)
    else:
        print(f"File {output_file} already exists. Skipping write operation.")

# Example usage
# create_unique_values_json(df, "provincia", "data/json/provincia.json")
# create_unique_values_json(df, "localidad", "data/json/localidad.json")
create_unique_values_json(df, "vendedor")
    



# #------ Transform data to json ------

# def transform_data(df, col_to_read, name_json):
#     unique_values = df[col_to_read].unique()
#     unique_values = unique_values[~pd.isnull(unique_values)]
#     unique_values = unique_values.tolist()
#     print(unique_values)
#     with open(f'data/{name_json}.json', 'w') as f:
#         json.dump(unique_values, f)

# transform_data(df, 't_iva', 't_iva')
# transform_data(df, 'servi_anterior', 'servi_anterior')
# transform_data(df, 'garantia', 'garantia')
# transform_data(df, 'provincia', 'provincia')




# #------ Load data from json to database ------
# marcas = json.load(open("data/json/brands_models_cleaned.json"))

# marca_list = []
# for marca in marcas:
#     marca_list.append(marca)

# #------ Filter wrong data ------

# # Filter only rows without marca in marca list

# # df = df[~df["marca"].isin(marca_list)]

# # Change the value where marca is equal to "Infiniti" to "Nissan"
# df.loc[df["marca"] == "Bmw", "marca"] = "BMW"
# df.loc[df["marca"] == "Toyoya", "marca"] = "Toyota"
# df.loc[df["marca"].isin(["Citroen", "Citröen"]) , "marca"] = "Citroën"
# df.loc[(df["marca"].isna()) & (df["modelo"] == "Q30"), "marca"] = "Infiniti"
# df.loc[(df["marca"].isna()) & (df["modelo"] == "Clio"), "marca"] = "Renault"

# # df = df[~df["marca"].isin(marca_list)]

# # print(df.loc[df["marca"].isna()])

# # print(df["marca"].unique().tolist())

