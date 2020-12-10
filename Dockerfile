FROM python:3.9-alpine as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# TODO remove git dependency once we can get PyExifTool from PyPI
RUN apk update && \
    apk add --no-cache postgresql-dev gcc git python3-dev musl-dev jpeg-dev zlib-dev
RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN mkdir -p /wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /tmp/requirements.txt


FROM python:3.9-alpine

ENV APP_HOME=/home/app

RUN apk update && apk add libpq jpeg
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media
COPY . $APP_HOME

RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app $APP_HOME
USER app
WORKDIR $APP_HOME
