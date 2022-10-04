FROM python:3.9-slim

ENV APP_NAME=bootstrap
# Define workdir
ENV WORKDIR=/home/${APP_NAME}/project
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Fix debconf warnings upon build
ARG DEBIAN_FRONTEND=noninteractive
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for project
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    netcat gcc \
 && rm -rf /var/lib/apt/lists/*

# Create a group and user to run app
RUN useradd --create-home ${APP_NAME}
ENV PATH=/home/${APP_NAME}/.local/bin:$PATH

# Change to a non-root user
USER ${APP_NAME}:${APP_NAME}

# install python dependencies
COPY requirements.txt ${WORKDIR}/requirements.txt
RUN pip install --upgrade pip \
 && pip install --ignore-installed -r ${WORKDIR}/requirements.txt

COPY --chown=origin ./src/app/ ${WORKDIR}/src/app/

WORKDIR ${WORKDIR}
