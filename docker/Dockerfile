FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip pytest-cov nbval pycodestyle

COPY . /usr/local/ubermagutil/
WORKDIR /usr/local/ubermagutil
RUN python3 -m pip install .
