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
from pytz import timezone
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


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
    spain_tz = timezone('Europe/Madrid')
    creation_time = datetime.datetime.now(spain_tz).strftime("%Y-%m-%d %H:%M:%S")
    
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

# Subir el archivo
file1 = drive.CreateFile({'title': 'ventas_report.pdf'})  # Cambia 'mi_archivo.txt' por el nombre de tu archivo
file1.SetContentFile('ventas_report.pdf')  # Cambia 'ruta/a/tu_archivo.txt' por la ruta de tu archivo
file1.Upload()

# Hacer el archivo público
file1.InsertPermission({
    'type': 'anyone',
    'value': 'anyone',
    'role': 'reader'
})
