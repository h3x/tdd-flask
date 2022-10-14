# pull official base image
FROM python:3.10.3-slim-buster

# Set working directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install System Dependancies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

# Add install Requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add app
COPY . .

# Add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh