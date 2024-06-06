# from catalog.models import Car, Brand
import pandas as pd
import json

# from catalog.models import Brand


# def transform_data(df, col_to_read, name_json):
#     unique_values = df[col_to_read].unique()
#     unique_values = unique_values[~pd.isnull(unique_values)]
#     unique_values = unique_values.tolist()
#     print(unique_values)
#     with open(f'data/{name_json}.json', 'w') as f:
#         json.dump(unique_values, f)

# transform_data(df, 'Tipo de IVA', 'iva')
# transform_data(df, 'Servicio anterior', 'servicio_anterior')
# transform_data(df, 'Garantía', 'garantia')


# ------ Load data from excel to database ------

# df = pd.read_excel("./data/Datos.xlsx", sheet_name="Export_datos").drop_duplicates().iloc[0:10, :]
df = pd.read_excel("./data/Datos.xlsx", sheet_name="Export_datos").drop_duplicates()

# df.drop(5469, inplace=True)

df = df.drop(df.index[5469])

print(df)

marcas = json.load(open("data/marcas_models_cleaned.json"))

marca_list = []
for marca in marcas:
    marca_list.append(marca)
    # Brand.objects.get_or_create(name=marca)
    # print(marca + ' creado')

# print(marca_list)

# Rename columns
df.rename(
    columns={
        "Matrícula": "matricula",
        "Chasis": "chasis",
        "Fecha matriculación": "f_matriculacion",
        # "Documentado": "documented",
        "Marca": "marca",
        "Color": "color",
        "Precio contado": "buy_price",
        "Precio financiado": "sale_price",
        "Kilómetros": "km",
        "Combustible": "combustible",
        "Cambio": "cambio",
        "Versión": "version",
        "Modelo": "modelo",
    },
    inplace=True,
)

#------ Filter wrong data ------

# Filter only rows without marca in marca list

# df = df[~df["marca"].isin(marca_list)]

# Change the value where marca is equal to "Infiniti" to "Nissan"
df.loc[df["marca"] == "Bmw", "marca"] = "BMW"
df.loc[df["marca"] == "Toyoya", "marca"] = "Toyota"
df.loc[df["marca"].isin(["Citroen", "Citröen"]) , "marca"] = "Citroën"
df.loc[(df["marca"].isna()) & (df["modelo"] == "Q30"), "marca"] = "Infiniti"
df.loc[(df["marca"].isna()) & (df["modelo"] == "Clio"), "marca"] = "Renault"

# df = df[~df["marca"].isin(marca_list)]

# print(df.loc[df["marca"].isna()])

# print(df["marca"].unique().tolist())

""" 
#------ Filter data ------
df = df[df["marca"].isin(marca_list)]

# print(df.shape)
# print(df.columns.to_list())


# print(df.columns.to_list())

# Select columns
df = df.loc[:, ["matricula", "chasis", "f_matriculacion", "marca", "color", "buy_price", "sale_price", "km", "combustible", "cambio", "version", "modelo"]]

# Create new column documented with default value True
df["documented"] = True

# Filter only complete rows
df = df.dropna()
print(df.shape)

# Send data to database

# for index, row in df.iterrows():
#     print(index)

# for index, row in df.iterrows():
#     marca = row["marca"]
#     marca = Brand.objects.get(name=marca)
#     Car.objects.get_or_create(
#         matricula=row["matricula"],
#         chasis=row["chasis"],
#         f_matriculacion=row["f_matriculacion"],
#         documented=row["documented"],
#         marca=marca,
#         color=row["color"],
#         buy_price=row["buy_price"],
#         sale_price=row["sale_price"],
#         km=row["km"],
#         combustible=row["combustible"],
#         cambio=row["cambio"],
#         version=row["version"],
#         modelo=row["modelo"],
#     )
    
    
 """
