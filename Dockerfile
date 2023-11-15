# Use an official Python runtime as a parent image
FROM python:3.11.0-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /code/

# Run the application
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
RUN python manage.py runserver
