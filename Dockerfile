FROM python:3.9.5-alpine

RUN mkdir /opt/flask-api/
WORKDIR /opt/flask-api/

COPY requirements.txt /opt/flask-api/requirements.txt

RUN apk update && apk add --no-cache --virtual .build-deps \
  build-base \
  make \
  gcc \
  python3-dev \
  musl-dev \
  postgresql-dev \
  && pip install --no-cache-dir -r requirements.txt \
  && apk del --no-cache .build-deps

COPY . .

EXPOSE 80

CMD [ "python3", "/opt/flask-api/run.py"]