FROM python:3.10
WORKDIR /app

RUN pip install -U pip && \
  pip install poetry
