# Se ejecuta con el comando: python manage.py shell < data/load_data.py

import json
from catalog.models import Brand, Car 
import pandas as pd

# with open('data/marcas_models.json', 'r') as file:
#     marcas = json.load(file)

# for marca_name in marcas:
#     Brand.objects.get_or_create(name=marca_name)
#     print(marca_name + ' creado')
    
def load_data_json(json_name, model):
    with open(f'data/{json_name}.json', 'r') as file:
        data = json.load(file)
    
    for item in data:
        model.objects.get_or_create(name=item)
        print(item + ' creado')

    return data

marcas = load_data_json('brands_models_cleaned', Brand)

df = pd.read_excel("./data/Datos.xlsx", sheet_name="Export_datos").drop_duplicates().iloc[0:10, :]

with open('column_dict.json', 'r') as f:
    nuevos_nombres = json.load(f)

df.rename(columns=nuevos_nombres, inplace=True)

""" df.rename(
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
) """

df = df.loc[:, ["matricula", "chasis", "f_matriculacion", "marca", "color", "buy_price", "sale_price", "km", "combustible", "cambio", "version", "modelo"]]
df["documented"] = True
df = df.dropna()

for index, row in df.iterrows():
    print(index)
    if row["marca"] in marcas:
        marca = row["marca"]
        marca = Brand.objects.get(name=marca)
        Car.objects.get_or_create(
            matricula=row["matricula"],
            chasis=row["chasis"],
            f_matriculacion=row["f_matriculacion"],
            documented=row["documented"],
            marca=marca,
            color=row["color"],
            buy_price=row["buy_price"],
            sale_price=row["sale_price"],
            km=row["km"],
            combustible=row["combustible"],
            cambio=row["cambio"],
            version=row["version"],
            modelo=row["modelo"],
        )
