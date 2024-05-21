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

df = pd.read_excel("./data/Datos.xlsx", sheet_name="Export_datos").drop_duplicates().iloc[0:10, :]
print(df.shape)

brands = json.load(open("data/brands_models_cleaned.json"))

brand_list = []
for brand in brands:
    brand_list.append(brand)
    # Brand.objects.get_or_create(name=brand)
    # print(brand + ' creado')

print(brand_list)

df = df[df["Marca"].isin(brand_list)]

# print(df.shape)
# print(df.columns.to_list())

# # Rename columns
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

# print(df.columns.to_list())

# Select columns
df = df.loc[:, ["matricula", "chassis", "registration_date", "brand", "color", "buy_price", "sale_price", "km", "fuel", "transmission", "version", "car_model"]]

# Create new column documented with default value True
df["documented"] = True

# Filter only complete rows
df = df.dropna()
print(df.shape)

# Send data to database

# for index, row in df.iterrows():
#     print(index)

# for index, row in df.iterrows():
#     brand = row["brand"]
#     brand = Brand.objects.get(name=brand)
#     Car.objects.get_or_create(
#         matricula=row["matricula"],
#         chassis=row["chassis"],
#         registration_date=row["registration_date"],
#         documented=row["documented"],
#         brand=brand,
#         color=row["color"],
#         buy_price=row["buy_price"],
#         sale_price=row["sale_price"],
#         km=row["km"],
#         fuel=row["fuel"],
#         transmission=row["transmission"],
#         version=row["version"],
#         car_model=row["car_model"],
#     )
    
    
