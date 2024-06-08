# Se ejecuta con el comando: python manage.py shell < data/load_data.py

import json
import pandas as pd
from catalog.models import Brand, Car
from sales.models import Province, Municipality, Saler, Client, Sales


# with open('data/brands_models_cleaned.json', 'r') as file:
#     marcas = json.load(file)

# for marca_name in marcas:
#     Brand.objects.get_or_create(name=marca_name)
#     print(marca_name + ' creado')


def load_data_json(json_name, model):
    with open(f"data/json/{json_name}.json", "r") as file:
        data = json.load(file)

    for item in data:
        model.objects.get_or_create(name=item)
        print(item + " creado")

    return data


marcas = load_data_json("brands_models", Brand)


def date_parser(x):
    return pd.to_datetime(x, format="%d/%m/%y").date()


# Carga los datos del archivo Excel
df = pd.read_excel(
    "./data/Principal.xlsx",
    sheet_name="Principal",
    parse_dates=True,
    date_format=date_parser,
)

# Elimina duplicados y selecciona las primeras 10 filas
df = df.drop_duplicates().iloc[0:10, :]

with open("data/json/column_dict.json", "r") as f:
    nuevos_nombres = json.load(f)

df.rename(columns=nuevos_nombres, inplace=True)

# df = df.loc[:, ["matricula", "chasis", "f_matriculacion", "marca", "color", "buy_price", "sale_price", "km", "combustible", "cambio", "version", "modelo"]]
# df["documented"] = True
# # df = df.dropna()

car_fields = [field.name for field in Car._meta.get_fields()]

# Crear una dataframe vacio igual que df para almacenar los errores de la carga
df_errores = pd.DataFrame(columns=df.columns)

for index, row in df.iterrows():
    car = Car()
    for field in car_fields:
        if field == "marca":
            try:
                brand = Brand.objects.get(name=row[field])
            except Brand.DoesNotExist:
                df_errores = df_errores.append(row)
                print(f"Marca {row[field]} no encontrada")
                continue
            
            setattr(car, field, brand)
        else:
            setattr(car, field, row[field])
    car.save()
    print(f"Coche {car.matricula} creado")

df_errores.to_excel("data/errores.xlsx", index=False)
