FROM python:3.10.10-slim-buster as quotes_wss_app

RUN mkdir /quotes_wss_app
COPY . /quotes_wss_app
WORKDIR /quotes_wss_app
RUN mkdir log
RUN touch /tmp/quotes.json

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
