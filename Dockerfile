# pull official base image
# Dockerfile for Marti App
#
# This Dockerfile is used to build an image for the Marti App.
# It is based on the official Python 3 image.

FROM python:3.11.3-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]