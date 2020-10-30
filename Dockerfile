FROM python:3.8-slim

RUN python -m pip install --upgrade pip

WORKDIR /srv/app

COPY ./app/requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./app .
RUN chmod +x ./entrypoint.sh