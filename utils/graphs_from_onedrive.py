#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image


# Read the CSV file from the shared link
principal = "https://cochesmalaga-my.sharepoint.com/:x:/g/personal/admin_cochesmalaga_onmicrosoft_com/EdxJ2pk55p1FuwZgdGaTIi4BlremkYZUHO88h1HmitehOg?download=1"
forma_pago="https://cochesmalaga-my.sharepoint.com/:x:/g/personal/admin_cochesmalaga_onmicrosoft_com/Ebj0vhlq-5pDpgkw6Qgv36cBjLCnd3oGL5M4a60gzKY-nA?download=1"


def get_dataframe_from_url(url):

    # Descargar el archivo
    response = requests.get(url)
    response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa

    # Leer el contenido del archivo en un DataFrame de pandas
    file = BytesIO(response.content)

    return file

principal = pd.read_csv(get_dataframe_from_url(principal), low_memory=False)

forma_pago = pd.read_csv(get_dataframe_from_url(forma_pago))

# %%

# Renombrar columnas
principal.rename(columns={'Matr_x00ed_cula': 'Matrícula', 
                          'En_x0020_stock': 'En stock', 
                          'Fecha_x0020_venta': 'Fecha venta',
                          'Listar_x0020_admin': 'Listar admin'}, inplace=True)

forma_pago.rename(columns={'Matr_x00ed_cula': 'Matrícula', 
                          'En_x0020_stock': 'En stock', 
                          'Fecha_x0020_venta': 'Fecha venta',
                          'Listar_x0020_admin': 'Listar admin'}, inplace=True)

# Cambiar el formato de la fecha de venta a datetime
principal['Fecha venta'] = pd.to_datetime(principal['Fecha venta'])

# %%

# Realizar el join de los dataframes
merged_df = pd.merge(principal, forma_pago, on='Matrícula', how='left')

filtered_df = merged_df.loc[(merged_df['Destino'] == 'Venta') & (merged_df['En stock'] == False) & (merged_df['Listar admin'] == False)].copy()  # noqa: E712

# %%
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

# Función para generar y guardar gráficos
def save_sales_plot(filtered_df, title, filename, date_filter_start, date_filter_end):
    date_filter_start = pd.to_datetime(date_filter_start)
    date_filter_end = pd.to_datetime(date_filter_end)
    filtered_data = filtered_df.loc[
        (filtered_df['Fecha venta'] >= date_filter_start) & 
        (filtered_df['Fecha venta'] <= date_filter_end)
    ]
    sales_per_vendor = filtered_data['Vendedor'].value_counts()

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    barplot = sns.barplot(x=sales_per_vendor.index, y=sales_per_vendor.values, color='skyblue')
    barplot.set_xlabel('Vendedor', fontsize=12)
    barplot.set_ylabel('Número de Ventas', fontsize=12)
    barplot.set_title(title, fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, fontsize=10)

    business_days = pd.bdate_range(date_filter_start, today, freq=bday_spain).day
    estimated_sales = len(business_days) * 0.7
    barplot.axhline(y=estimated_sales, color='r', linestyle='--', label='Ventas estimadas')
    barplot.set_ylim(0, max(max(sales_per_vendor.values), estimated_sales + 1))
    barplot.legend()

    plt.savefig(filename)
    plt.close()

# Generar y guardar los gráficos
save_sales_plot(filtered_df, 'Ventas por Vendedor en la Semana Actual', 'ventas_semanal.png', today - datetime.timedelta(days=today.weekday()), today)
save_sales_plot(filtered_df, 'Ventas por Vendedor en el Mes Actual', 'ventas_mensual.png', today.replace(day=1), today)
save_sales_plot(filtered_df, 'Ventas por Vendedor en el Año Actual', 'ventas_anual.png', today.replace(month=1, day=1), today)

# Crear un PDF con los gráficos y la fecha de creación
def create_pdf(output_filename, images):
    pdf = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    creation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for image in images:
        img = Image.open(image)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        
        # Ajustar las dimensiones para mantener la relación de aspecto
        if img_width > width or img_height > height:
            img_width = width
            img_height = width * aspect
            if img_height > height:
                img_height = height
                img_width = height / aspect
        
        x = (width - img_width) / 2
        y = (height - img_height) / 2
        pdf.drawImage(image, x, y, img_width, img_height)
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(30, 750, f"PDF creado el: {creation_time}")
        pdf.showPage()
    pdf.save()

# Crear el PDF
create_pdf("ventas_report.pdf", ["ventas_semanal.png", "ventas_mensual.png", "ventas_anual.png"])

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

# Asegurar que el gráfico llega a los valores estimados de ventas
barplot.set_ylim(0, max(max(sales_per_vendor.values), estimated_sales + 1))

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

# Asegurar que el gráfico llega a los valores estimados de ventas
barplot.set_ylim(0, max(max(sales_per_vendor.values), estimated_sales + 1))

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

# Asegurar que el gráfico llega a los valores estimados de ventas
barplot.set_ylim(0, max(max(sales_per_vendor.values), estimated_sales + 1))

# Añadir una leyenda
barplot.legend()

# Mostrar el gráfico
plt.show()

# %%

# Generar un pdf con los tres gráficos anteriores y que indique cuando se creo y guardarlo en la carpeta de trabajo
from matplotlib.backends.backend_pdf import PdfPages

# Crear un objeto PdfPages
pdf_pages = PdfPages('ventas_por_vendedor.pdf')

# Crear los tres gráficos
fig1 = plt.figure(figsize=(10,6))
sns.set_style("whitegrid")
barplot = sns.barplot(x=sales_per_vendor.index, y=sales_per_vendor.values, color='skyblue')
barplot.set_xlabel('Vendedor', fontsize=12)
barplot.set_ylabel('Número de Ventas', fontsize=12)
barplot.set_title('Ventas por Vendedor en la Semana Actual', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, fontsize=10)
barplot.axhline(y=estimated_sales, color='r', linestyle='--', label='Ventas estimadas')
barplot.set_ylim(0, max(max(sales_per_vendor.values), estimated_sales + 1))
barplot.legend()
pdf_pages.savefig(fig1)

fig2 = plt.figure(figsize=(10,6))


