#!/bin/sh

# Construir la imagen de Docker
docker build -t my-python-script .

# Ejecutar el contenedor de Docker
docker run --rm -v $(pwd):/app my-python-script
