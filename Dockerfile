FROM python:3.14.0a1-slim-bookworm

LABEL maintainer="tomer.klein@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LOG_LEVEL "DEBUG"
ENV NOTIFIERS ""
ENV LOCATION ""
ENV LANGUAGE ""

RUN apt update -yqq

RUN apt install -yqq libsndfile1-dev && \
    apt install -yqq libffi-dev && \
    apt install -yqq libssl-dev

RUN mkdir -p /app/data

RUN  pip3 install --upgrade pip --no-cache-dir && \
     pip3 install --upgrade setuptools --no-cache-dir

COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

COPY app /app

WORKDIR /app

ENTRYPOINT python app.py
