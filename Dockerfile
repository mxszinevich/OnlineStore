FROM python:3.8-alpine
WORKDIR /usr/src/online_store

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev g++
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/online_store
RUN pip install -r requirements.txt

COPY . /usr/src/online_store