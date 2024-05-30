# Usa una imagen base oficial de Python con las versiones necesarias de Python y pip
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos requeridos a /app
COPY . /app

# Instala las dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    cron \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crear un usuario no root y cambiar a ese usuario
RUN useradd -m myuser
USER myuser

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Volver al usuario root para configurar cron
USER root

# Añade el archivo crontab al directorio cron.d
COPY crontab /etc/cron.d/my-cron-job

# Da permiso de ejecución al archivo crontab
RUN chmod 0644 /etc/cron.d/my-cron-job

# Aplica el crontab
RUN crontab /etc/cron.d/my-cron-job

# Crea el directorio para los logs del cron
RUN touch /var/log/cron.log

# Ejecuta el comando para iniciar cron y mantener el contenedor en ejecución
CMD cron && tail -f /var/log/cron.log
