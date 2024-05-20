FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code

COPY . /code

EXPOSE 8000