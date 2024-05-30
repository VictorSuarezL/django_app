#%%
# from heapq import merge
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday
from pandas.tseries.offsets import CustomBusinessDay

#%%

# Read the CSV file from the shared link
url = "https://cochesmalaga-my.sharepoint.com/:x:/g/personal/admin_cochesmalaga_onmicrosoft_com/EdxJ2pk55p1FuwZgdGaTIi4BlremkYZUHO88h1HmitehOg?download=1"

import requests
import pandas as pd
from io import BytesIO

# Descargar el archivo
response = requests.get(url)
response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa

# Leer el contenido del archivo en un DataFrame de pandas
file = BytesIO(response.content)
df = pd.read_csv(file, encoding='utf-8')

# Mostrar las primeras filas del DataFrame
print(df.head())


#%%

principal = pd.read_csv('/Users/victorsanz/Downloads/Principal.csv', parse_dates=['Fecha_x0020_venta'], dayfirst=True, low_memory=False)
forma_pago = pd.read_csv('/Users/victorsanz/Downloads/Forma pago.csv')

#%%
# Realizar el join de los dataframes
merged_df = pd.merge(principal, forma_pago, on='Matrícula', how='left')

filtered_df = merged_df.loc[(merged_df['Destino'] == 'Venta') & (merged_df['En stock'] == "False") & (merged_df['Listar admin'] == "False")].copy()


#%%
# Añadir las columnas calculadas
filtered_df['Calcu'] = pd.to_datetime(filtered_df['Fecha venta']).dt.month
filtered_df['Calcu2'] = pd.to_datetime(filtered_df['Fecha venta']).dt.year


#%%
# Los vendedores deben hacer 0.7 ventas por día laborale. Indicar en la parte superior de las gráficas cuántas
# ventas deberían llevar (en función del día del mes en el estemos) 
# ! ¿Los sábados cuentan como día laborables?

# Calcular el número de día laborable del mes actual
class SpanishHolidays(AbstractHolidayCalendar):
    rules = [
        Holiday('New Year', month=1, day=1),
        Holiday('Epiphany', month=1, day=6),
        # Holiday('Good Friday', month=1, day=1, offset=[Easter(), Day(-2)]),
        Holiday('Labour Day', month=5, day=1),
        Holiday('Assumption of Mary', month=8, day=15),
        Holiday('National Day', month=10, day=12),
        Holiday('All Saints Day', month=11, day=1),
        Holiday('Constitution Day', month=12, day=6),
        Holiday('Immaculate Conception', month=12, day=8),
        Holiday('Christmas Day', month=12, day=25)
    ]

# Create custom business day with Spanish holidays
bday_spain = CustomBusinessDay(calendar=SpanishHolidays())

today = datetime.date.today()

#%%
# Gráfica 1: Deben aparecer todos los vendedores, indicando las ventas que lleva cda uno esa semana

# Filtrar los datos de la semana actual
week_start = today - datetime.timedelta(days=today.weekday())
week_end = week_start + datetime.timedelta(days=6)


# Contar el número de business days en business_days
business_days = pd.bdate_range(week_start, today, freq=bday_spain).day
estimated_sales = len(business_days) * 0.7

week_start = pd.to_datetime(week_start)
week_end = pd.to_datetime(week_end)

filtered_week = filtered_df.loc[(filtered_df['Fecha venta'] >= week_start) & (filtered_df['Fecha venta'] <= week_end)]


# Calcular el número de ventas por vendedor en la semana actual
sales_per_vendor = filtered_week['Vendedor'].value_counts()

# Crear el gráfico de barras
plt.figure(figsize=(10,6))
sns.set_style("whitegrid")
barplot = sns.barplot(x=sales_per_vendor.index, y=sales_per_vendor.values, color='skyblue')

# Añadir etiquetas y título
barplot.set_xlabel('Vendedor', fontsize=12)
barplot.set_ylabel('Número de Ventas', fontsize=12)
barplot.set_title('Ventas por Vendedor en la Semana Actual', fontsize=14, fontweight='bold')

# Rotar las etiquetas del eje x
plt.xticks(rotation=45, fontsize=10)

# Añadir una línea horizontal
barplot.axhline(y=estimated_sales, color='r', linestyle='--', label='Ventas estimadas')

# Añadir una leyenda
barplot.legend()

# Mostrar el gráfico
plt.show()

# %%
# Gráfica 2: Deben aparecer todos los vendedores, indicando las ventas que lleva cda uno ese mes

# Filtrar los datos del mes actual
month_start = today.replace(day=1)
month_end = month_start + pd.DateOffset(months=1) - pd.DateOffset(days=1)

# Contar el número de business days en business_days
business_days = pd.bdate_range(month_start, today, freq=bday_spain).day
estimated_sales = len(business_days) * 0.7

month_start = pd.to_datetime(month_start) 
month_end = pd.to_datetime(month_end)

filtered_month = filtered_df.loc[(filtered_df['Fecha venta'] >= month_start) & (filtered_df['Fecha venta'] <= month_end)]

# Calcular el número de ventas por vendedor en el mes actual
sales_per_vendor = filtered_month['Vendedor'].value_counts()

# Crear el gráfico de barras
plt.figure(figsize=(10,6))
sns.set_style("whitegrid")
barplot = sns.barplot(x=sales_per_vendor.index, y=sales_per_vendor.values, color='skyblue')

# Añadir etiquetas y título
barplot.set_xlabel('Vendedor', fontsize=12)
barplot.set_ylabel('Número de Ventas', fontsize=12)
barplot.set_title('Ventas por Vendedor en el Mes Actual', fontsize=14, fontweight='bold')

# Rotar las etiquetas del eje x
plt.xticks(rotation=45, fontsize=10)

# Añadir una línea horizontal
barplot.axhline(y=estimated_sales, color='r', linestyle='--', label='Ventas estimadas')

# Añadir una leyenda
barplot.legend()

# Mostrar el gráfico
plt.show()

# %%
# Gráfica 3: Deben aparecer todos los vendedores, indicando las ventas que lleva cda uno ese año

# Filtrar los datos del año actual
year_start = today.replace(month=1, day=1)
year_end = today.replace(month=12, day=31)

# Contar el número de business days en business_days
business_days = pd.bdate_range(year_start, today, freq=bday_spain).day
estimated_sales = len(business_days) * 0.7

year_start = pd.to_datetime(year_start)
year_end = pd.to_datetime(year_end)

filtered_year = filtered_df.loc[(filtered_df['Fecha venta'] >= year_start) & (filtered_df['Fecha venta'] <= year_end)]

# Calcular el número de ventas por vendedor en el año actual
sales_per_vendor = filtered_year['Vendedor'].value_counts()

# Crear el gráfico de barras
plt.figure(figsize=(10,6))
sns.set_style("whitegrid")
barplot = sns.barplot(x=sales_per_vendor.index, y=sales_per_vendor.values, color='skyblue')

# Añadir etiquetas y título
barplot.set_xlabel('Vendedor', fontsize=12)
barplot.set_ylabel('Número de Ventas', fontsize=12)
barplot.set_title('Ventas por Vendedor en el Año Actual', fontsize=14, fontweight='bold')

# Rotar las etiquetas del eje x
plt.xticks(rotation=45, fontsize=10)

# Añadir una línea horizontal
barplot.axhline(y=estimated_sales, color='r', linestyle='--', label='Ventas estimadas')

# Añadir una leyenda
barplot.legend()

# Mostrar el gráfico
plt.show()

# Crear el gráfico de barras
plt.figure(figsize=(10,6))
sns.set_style("whitegrid")
barplot = sns.barplot(x=sales_per_vendor.index, y=sales_per_vendor.values, color='skyblue')

# Añadir etiquetas y título
barplot.set_xlabel('Vendedor', fontsize=12)
barplot.set_ylabel('Número de Ventas', fontsize=12)
barplot.set_title('Ventas por Vendedor en el Año Actual', fontsize=14, fontweight='bold')

# Rotar las etiquetas del eje x
plt.xticks(rotation=45, fontsize=10)

# Añadir una línea horizontal
barplot.axhline(y=estimated_sales, color='r', linestyle='--', label='Ventas estimadas')

# Añadir una leyenda
barplot.legend()

# Mostrar el gráfico
plt.show()