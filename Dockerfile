FROM python:3.11.0-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y postgresql-contrib && rm -rf /var/lib/apt/lists/*
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /code/
