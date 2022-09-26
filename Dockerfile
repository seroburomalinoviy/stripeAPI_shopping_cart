###########
# BUILDER #
###########
# pull official base image
FROM python:3.9.13-alpine as builder
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
#########
# FINAL #
#########
# pull official base image
FROM python:3.9.13-alpine
# create directory for the app user
RUN mkdir -p /home/app
# create the app user
RUN addgroup -S app && adduser -S app -G app
# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
# copy project
COPY . $APP_HOME
# chown all the files to the app user
RUN chown -R app:app $APP_HOME
# change to the app user
USER app