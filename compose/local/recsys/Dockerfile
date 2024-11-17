FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        postgresql-client \
        libpq-dev \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements /requirements
RUN pip install -r /requirements/recsys.txt

COPY ./compose/local/recsys/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/recsys/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app

