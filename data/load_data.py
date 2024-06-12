# # Se ejecuta con el comando: python manage.py shell < data/load_data.py

import datetime
import json
from django.db.utils import IntegrityError
import pandas as pd
from catalog.models import Brand, Car
from sales.models import Sales, Client, Province, Municipality

def load_data_json(json_name, model):
    with open(f"data/json/{json_name}.json", "r") as file:
        data = json.load(file)

    for item in data:
        model.objects.get_or_create(name=item)
        print(item + " creado")

    return data

# Saler.objects.all().delete()


marcas = load_data_json("brands_models", Brand)
# vendedores = load_data_json("vendedor", Saler)


def load_data_json(json_name, model):
    with open(f"data/json/{json_name}.json", "r") as file:
        data = json.load(file)

    provincias = data.get("provincia", [])
    
    for provincia in provincias:
        model.objects.get_or_create(name=provincia)
        print(provincia + " creado")

    return provincias

provincias = load_data_json("provincia", Province)

Car.objects.all().delete()

def date_parser(x):
    return pd.to_datetime(x, format="%d/%m/%y").date().isoformat()


# Carga los datos del archivo Excel
df = pd.read_excel(
    "./data/Principal.xlsx",
    sheet_name="Principal",
    parse_dates=True,
    date_format=date_parser,
)
# Elimina duplicados y selecciona las primeras 10 filas

with open("data/json/column_dict.json", "r") as f:
    nuevos_nombres = json.load(f)

# Renombrar y seleccionar solo las columnas incluidas en el diccionario
df = df.rename(columns=nuevos_nombres)
df = df[nuevos_nombres.values()]

# Seleccionar donde vendedor no sea nan
df = df[df["vendedor"].notna()]
df = df.drop_duplicates().iloc[-10:, :]


# Cambiar en df valor de columna marca si coincide con Citroen cambiar por Citroën y Bmw por BMW
df["marca"] = df["marca"].replace("Bmw", "BMW")
df["marca"] = df["marca"].replace("Citroen", "Citroën")
df["marca"] = df["marca"].replace("Toyoya", "Toyota")

car_fields = [field.name for field in Car._meta.get_fields()]


# Crear una dataframe vacio con las columnas de df para almacenar los errores de la carga
df_errores = pd.DataFrame(columns=df.columns)

for index, row in df.iterrows():
    car = Car()
    has_error = False  # Bandera para detectar errores en la fila actual
    
    for field in car_fields:
        if field in row:
            value = row[field]
            
            if field == "marca":
                try:
                    brand = Brand.objects.get(name=value)
                    setattr(car, field, brand)
                except Brand.DoesNotExist:
                    df_errores = pd.concat([df_errores, pd.DataFrame([row])], ignore_index=True)
                    print(f"Marca {value} no encontrada en fila {index}")
                    has_error = True
                    break  # Sal del bucle de campos si la marca no existe
            
            else:
                if pd.isnull(value):
                    value = None  # Asignar None si el valor es 'nan'
                setattr(car, field, value)
    
    if not has_error:
        try:
            car.save()
            print(f"Coche {car.matricula} creado")
        except IntegrityError as e:
            df_errores = pd.concat([df_errores, pd.DataFrame([row])], ignore_index=True)
            print(f"Error al crear el coche {car.matricula}: {e}")

# Obtener todos los campos del modelo Sales, excluyendo 'id' y 'car'
sales_fields = [field.name for field in Sales._meta.get_fields() if field.name != 'id' and field.name != 'car']

for index, row in df.iterrows():  # Supongamos que df es tu DataFrame para Sales
    sales = Sales()
    has_error = False  # Bandera para detectar errores en la fila actual

    # Manejo especial para el campo 'car'
    try:
        car = Car.objects.get(matricula=row["matricula"])
        sales.car = car
    except Car.DoesNotExist:
        df_errores = pd.concat([df_errores, pd.DataFrame([row])], ignore_index=True)
        print(f"Coche con matrícula {row['matricula']} no encontrado en fila {index}")
        has_error = True

    # Si no hubo error en la asignación del coche, continuar con los demás campos
    if not has_error:
        for field in sales_fields:
            if field in row:
                value = row[field]
                if pd.isnull(value):
                    value = None  # Asignar None si el valor es 'nan'
                setattr(sales, field, value)

        try:
            sales.save()
            print(f"Venta del coche {index} registrada")
        except IntegrityError as e:
            df_errores = pd.concat([df_errores, pd.DataFrame([row])], ignore_index=True)
            print(f"Error al registrar la venta del coche {index}: {e}")
