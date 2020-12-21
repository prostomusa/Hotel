FROM python:3.8.5-alpine
# set work directory
WORKDIR /usr/src/Hotel
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt
RUN apk add --no-cache tzdata
ENV TZ Europe/Moscow
# copy project
COPY . .