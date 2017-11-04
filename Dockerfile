FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip pytest-cov nbval numpy

COPY . /usr/local/joommfutil/
WORKDIR /usr/local/joommfutil
RUN python3 -m pip install .
