FROM python:3.11-slim-buster

RUN apt update
RUN apt install -y libpq-dev cron g++ build-essential

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .