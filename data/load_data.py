# # Se ejecuta con el comando: python manage.py shell < data/load_data.py

# import datetime
# import json
# from django.db.utils import IntegrityError
# import pandas as pd
# from catalog.models import Brand, Car
# # from sales.models import Province, Municipality, Saler, Client, Sales


# # with open('data/brands_models_cleaned.json', 'r') as file:
# #     marcas = json.load(file)

# # for marca_name in marcas:
# #     Brand.objects.get_or_create(name=marca_name)
# #     print(marca_name + ' creado')


# def load_data_json(json_name, model):
#     with open(f"data/json/{json_name}.json", "r") as file:
#         data = json.load(file)

#     for item in data:
#         model.objects.get_or_create(name=item)
#         print(item + " creado")

#     return data


# marcas = load_data_json("brands_models", Brand)


# def date_parser(x):
#     return pd.to_datetime(x, format="%d/%m/%y").date().isoformat()


# # Carga los datos del archivo Excel
# df = pd.read_excel(
#     "./data/Principal.xlsx",
#     sheet_name="Principal",
#     parse_dates=True,
#     date_format=date_parser,
# )

# # Elimina duplicados y selecciona las primeras 10 filas
# df = df.drop_duplicates().iloc[-100:, :]

# with open("data/json/column_dict.json", "r") as f:
#     nuevos_nombres = json.load(f)

# df.rename(columns=nuevos_nombres, inplace=True)

# # df = df.loc[:, ["matricula", "chasis", "f_matriculacion", "marca", "color", "buy_price", "sale_price", "km", "combustible", "cambio", "version", "modelo"]]
# # df["documented"] = True
# # df = df.dropna()

# # Seleccionar filas con f_matriculacion, f_compra, f_ultima_itv y f_prox_itv no nulas
# # df = df.dropna(subset=["f_matriculacion", "f_compra", "f_ultima_itv", "f_prox_itv"])

# car_fields = [field.name for field in Car._meta.get_fields()]


# # Crear una dataframe vacio igual que df para almacenar los errores de la carga
# df_errores = pd.DataFrame(columns=df.columns)

# for index, row in df.iterrows():
#     car = Car()
#     for field in car_fields:
#         if field in row:
#             if field == "marca":
#                 try:
#                     brand = Brand.objects.get(name=row[field])
#                 except Brand.DoesNotExist:
#                     df_errores = pd.concat([df_errores, pd.DataFrame(row).transpose()])
#                     print(f"Marca {row[field]} no encontrada")
#                     continue
                
#                 setattr(car, field, brand)
#             else:
#                 value = row[field]
#                 if pd.isnull(value):  # Check if the value is 'nan'
#                     value = None  # Assign a default value or None
#                 setattr(car, field, value)
#     try:
#         car.save()
#         print(f"Coche {car.matricula} creado")
#     except IntegrityError:
#         df_errores = pd.concat([df_errores, pd.DataFrame(row).transpose()])
#         print(f"Coche {car.matricula} error")
#         pass
        

# df_errores.to_excel("data/errores.xlsx", index=False)

import datetime
import json
from django.db.utils import IntegrityError
import pandas as pd
from catalog.models import Brand, Car

Car.objects.all().delete()

def load_data_json(json_name, model):
    with open(f"data/json/{json_name}.json", "r") as file:
        data = json.load(file)
    for item in data:
        model.objects.get_or_create(name=item)
        print(item + " creado")
    return data

marcas = load_data_json("brands_models", Brand)

def date_parser(x):
    return pd.to_datetime(x, format="%d/%m/%y").date().isoformat()

df = pd.read_excel(
    "./data/Principal.xlsx",
    sheet_name="Principal",
    parse_dates=True,
    date_format=date_parser,
)

df = df.drop_duplicates().iloc[-100:, :]

with open("data/json/column_dict.json", "r") as f:
    nuevos_nombres = json.load(f)

df.rename(columns=nuevos_nombres, inplace=True)

car_fields = [field.name for field in Car._meta.get_fields()]
errores = []

def assign_value(car, field, value):
    if pd.isnull(value):
        value = None
    setattr(car, field, value)

brand_cache = {brand.name: brand for brand in Brand.objects.all()}
cars_to_create = []

for index, row in df.iterrows():
    car = Car()
    has_error = False
    
    for field in car_fields:
        if field in row:
            if field == "marca":
                brand_name = row[field]
                brand = brand_cache.get(brand_name)
                if not brand:
                    errores.append(row.to_dict())
                    print(f"Marca {brand_name} no encontrada")
                    has_error = True
                    break
                assign_value(car, field, brand)
            else:
                assign_value(car, field, row[field])
    
    if not has_error:
        cars_to_create.append(car)
    else:
        errores.append(row.to_dict())

try:
    Car.objects.bulk_create(cars_to_create)
except IntegrityError as e:
    print(f"Error al crear los coches: {e}")
    for car in cars_to_create:
        try:
            car.save()
        except IntegrityError:
            print(f"Coche {car.matricula} error")
            errores.append({field: getattr(car, field, None) for field in car_fields})

# Guardar errores en Excel
if errores:
    df_errores = pd.DataFrame(errores)
    
    # Eliminar información de zona horaria de las columnas datetime
    for col in df_errores.select_dtypes(include=['datetimetz']).columns:
        df_errores[col] = df_errores[col].dt.tz_localize(None)
    
    df_errores.to_excel("data/errores.xlsx", index=False)
