# This Dockerfile is used for Binder only. Dockerfile for tests and
# builds is in docker directory.

FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip pytest-cov nbval numpy

COPY . /usr/local/joommfutil/
WORKDIR /usr/local/joommfutil
RUN python3 -m pip install .

# Commands to make Binder work.
RUN pip install --no-cache-dir notebook==5.*
ENV NB_USER finmaguser
ENV NB_UID 1000
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
RUN chown -R ${NB_UID} /usr/local/joommfutil
USER ${NB_USER}

WORKDIR /usr/local/joommfutil