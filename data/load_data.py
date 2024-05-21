# Se ejecuta con el comando: python manage.py shell < data/load_data.py

import json
from catalog.models import Brand, Car 
import pandas as pd

# with open('data/brands_models.json', 'r') as file:
#     brands = json.load(file)

# for brand_name in brands:
#     Brand.objects.get_or_create(name=brand_name)
#     print(brand_name + ' creado')
    
def load_data_json(json_name, model):
    with open(f'data/{json_name}.json', 'r') as file:
        data = json.load(file)
    
    for item in data:
        model.objects.get_or_create(name=item)
        print(item + ' creado')

    return data

brands = load_data_json('brands_models_cleaned', Brand)

df = pd.read_excel("./data/Datos.xlsx", sheet_name="Export_datos").drop_duplicates().iloc[0:10, :]

df.rename(
    columns={
        "Matrícula": "matricula",
        "Chasis": "chassis",
        "Fecha matriculación": "registration_date",
        # "Documentado": "documented",
        "Marca": "brand",
        "Color": "color",
        "Precio contado": "buy_price",
        "Precio financiado": "sale_price",
        "Kilómetros": "km",
        "Combustible": "fuel",
        "Cambio": "transmission",
        "Versión": "version",
        "Modelo": "car_model",
    },
    inplace=True,
)

df = df.loc[:, ["matricula", "chassis", "registration_date", "brand", "color", "buy_price", "sale_price", "km", "fuel", "transmission", "version", "car_model"]]
df["documented"] = True
df = df.dropna()

for index, row in df.iterrows():
    print(index)
    if row["brand"] in brands:
        brand = row["brand"]
        brand = Brand.objects.get(name=brand)
        Car.objects.get_or_create(
            matricula=row["matricula"],
            chassis=row["chassis"],
            registration_date=row["registration_date"],
            documented=row["documented"],
            brand=brand,
            color=row["color"],
            buy_price=row["buy_price"],
            sale_price=row["sale_price"],
            km=row["km"],
            fuel=row["fuel"],
            transmission=row["transmission"],
            version=row["version"],
            car_model=row["car_model"],
        )