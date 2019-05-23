FROM python:3

RUN mkdir /work

COPY . /work
WORKDIR work