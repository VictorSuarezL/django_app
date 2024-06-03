#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay
import requests
from io import BytesIO
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from pytz import timezone
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

import sales


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

today = datetime.date.today()

# Quitar los vendedores cuyo valor sea Álvaro, Martín, Martin y Sandra
filtered_df = filtered_df.loc[~filtered_df["Vendedor"].isin(["Álvaro", 
                                                             "Martín", 
                                                             "Martin", 
                                                             "David López",
                                                             "Rocío",
                                                             "Sandra"])]

# Función para generar y guardar gráficos
def save_sales_plot(filtered_df, title, filename, date_filter_start, date_filter_end):
    date_filter_start = pd.to_datetime(date_filter_start)
    date_filter_end = pd.to_datetime(date_filter_end)
    filtered_data = filtered_df.loc[
        (filtered_df['Fecha venta'] >= date_filter_start) & 
        (filtered_df['Fecha venta'] <= date_filter_end)
    ]
    sales_per_vendor = filtered_data['Vendedor'].value_counts().sort_index()
    
    # Si sales_per_vendor está vacío, crear un DataFrame vacío con los vendedores como índice y sus ventas en 0
    if sales_per_vendor.empty:
        sales_per_vendor = pd.Series(0, index=filtered_df['Vendedor'].unique()).sort_index()
        sales_per_vendor = sales_per_vendor.loc[~sales_per_vendor.index.isin(["David López", "Rocío", "Sandra"])]

    plt.figure(figsize=(4, 3))
    sns.set_style("whitegrid")
    barplot = sns.barplot(x=sales_per_vendor.index, y=sales_per_vendor.values, color='skyblue', width=0.5)
    barplot.set_xlabel('Vendedor')
    barplot.set_ylabel('Número de Ventas')
    barplot.set_title(title)
    plt.xticks(rotation=45, fontsize=10)
    # Añadir el número de ventas encima de cada barra

    business_days = np.busday_count(date_filter_start.strftime('%Y-%m-%d'), date_filter_end.strftime('%Y-%m-%d'))
    estimated_sales = business_days * 0.8
    
    if estimated_sales != 0:
        
        for index, value in enumerate(sales_per_vendor.values):
            barplot.text(index, value + 0.1, str(value), ha='center', va='bottom')
            
    if filename == 'ventas_semanal.png':
        ventas = 4
    elif filename == 'ventas_mensual.png':
        ventas = 17
    elif filename == 'ventas_anual.png':
        ventas = 204
        
    if sales_per_vendor.empty:
        max_value = max(estimated_sales, ventas)
    else:
        max_value = max(sales_per_vendor.values.max(), estimated_sales, ventas)    

    if estimated_sales != 0:
        barplot.axhline(y=estimated_sales, color='r', linestyle='--', label='Ventas por día laborable')
    barplot.axhline(y=ventas, color='g', linestyle='-', label='Meta de ventas')
    barplot.set_ylim(0, max_value + 2)
    barplot.legend()
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Generar y guardar los gráficos
save_sales_plot(filtered_df, 'Ventas por Vendedor en la Semana Actual', 'ventas_semanal.png', today - datetime.timedelta(days=today.weekday()), today)
save_sales_plot(filtered_df, 'Ventas por Vendedor en el Mes Actual', 'ventas_mensual.png', today.replace(day=1), today)
save_sales_plot(filtered_df, 'Ventas por Vendedor en el Año Actual', 'ventas_anual.png', today.replace(month=1, day=1), today)

# %%
from reportlab.lib.pagesizes import A4, landscape

def create_pdf(output_filename, images):
    pdf = canvas.Canvas(output_filename, pagesize=landscape(A4))

    width, height = landscape(A4)
    spain_tz = timezone('Europe/Madrid')
    creation_time = datetime.datetime.now(spain_tz).strftime("%H:%M:%S %d/%m/%Y ")

    img_width = width / len(images)
    
    for i, image in enumerate(images):
        img = Image.open(image)
        img_height = img.size[1] * (img_width / img.size[0])  # maintain aspect ratio

        # Ajustar las dimensiones para mantener la relación de aspecto
        if img_height > height:
            img_height = height
            img_width = height * (img.size[0] / img.size[1])  # maintain aspect ratio

        x = i * img_width
        y = (height - img_height) / 2
        pdf.drawImage(image, x, y, img_width, img_height)

    pdf.setFont("Helvetica", 10)
    pdf.drawString(30, height - 30, f"Actualizado el: {creation_time}")
    pdf.drawString(30, height - 50, f"El número de ventas estimadas de este mes es de {np.busday_count(today.replace(day=1), today) * 0.8}")
    pdf.showPage()
    pdf.save()

# Crear el PDF
create_pdf("ventas_report.pdf", ["ventas_semanal.png", "ventas_mensual.png", "ventas_anual.png"])

# %%


# Set working directory to the actual file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Autenticar y crear la instancia de GoogleDrive
gauth = GoogleAuth()

# Cargar configuración de cliente
gauth.LoadClientConfigFile('client_secrets.json')

# Usar el método de autenticación basado en línea de comandos
gauth.CommandLineAuth()

drive = GoogleDrive(gauth)

# ID del archivo existente
file_id = '1vhxlh3KaDQGRjl9eOnN-i4vBIMEum3Zx'

# Crear un objeto de archivo con el ID del archivo existente
file1 = drive.CreateFile({'id': file_id})

# Establecer el contenido del archivo
file1.SetContentFile('ventas_report.pdf')

# Subir el archivo, esto sobrescribirá el archivo existente
file1.Upload()

# Hacer el archivo público
file1.InsertPermission({
    'type': 'anyone',
    'value': 'anyone',
    'role': 'reader'
})

# Borrar los archivos locales
os.remove('ventas_report.pdf')
os.remove('ventas_semanal.png')
os.remove('ventas_mensual.png')
os.remove('ventas_anual.png')

print('Archivo subido y compartido con éxito')

# %%
