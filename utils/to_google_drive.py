from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

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
file1 = drive.CreateFile({'title': 'requirements.txt'})  # Cambia 'mi_archivo.txt' por el nombre de tu archivo
file1.SetContentFile('../requirements.txt')  # Cambia 'ruta/a/tu_archivo.txt' por la ruta de tu archivo
file1.Upload()

# Hacer el archivo público
file1.InsertPermission({
    'type': 'anyone',
    'value': 'anyone',
    'role': 'reader'
})

# Obtener el enlace público
print('Enlace público: %s' % file1['alternateLink'])