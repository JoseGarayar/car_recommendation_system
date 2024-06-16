FROM python:3.12.2-alpine3.19

ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev

RUN addgroup -S flask \
    && adduser -S -G flask flask

COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/flask/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./app1 /app

RUN chown -R flask /app

USER flask

WORKDIR /app
