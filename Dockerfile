FROM python:3.8.5-slim-buster
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/code
RUN mkdir -p /app/run
WORKDIR /app/code

RUN apt update -y && apt -y install \
    cron \
    vim-tiny \
    python3-pip \
    libexpat1 \
    ssl-cert \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-setuptools \
    git \
    gcc \
    libxml2-dev \
    libxslt-dev
RUN apt-get update -y
RUN apt-get install -y gettext
RUN apt update -y && apt -y install cmake protobuf-compiler
COPY ./src/DataBet/requirements.txt /app/code/
RUN pip install -r requirements.txt

## clear cache OS
RUN apt-get purge -y --auto-remove && \
    rm -rf /var/lib/apt/lists/*

COPY ./src/DataBet/ /app/code/

# COPY cron_tab /app/code/
# RUN crontab cron_tab

CMD [ "sh", "-c", "python manage.py cache_clear; python /app/code/manage.py migrate; uwsgi --show-config --ini uwsgi.ini" ]