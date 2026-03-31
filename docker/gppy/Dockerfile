#
# Copyright TLM Partners, Inc. All Rights Reserved
#
# Use an LTS image for the base
FROM python:3.13-alpine AS base

FROM base AS builder
ENV SERVICE_NAME="gppy"
ENV PIP_ROOT_USER_ACTION=ignore

RUN apk update; \
    apk upgrade
RUN apk add busybox \
    curl \
    wget
# pyo dependencies
# RUN apk add gcc libc-dev
# portaudio portaudio-dev \
# libsndfile libsndfile-dev \
# portmidi portmidi-dev \
# liblo liblo-dev


COPY installs/* /tmp
RUN ls -l /tmp

RUN python3 -m pip install --break-system-packages --upgrade -r /tmp/requirements.txt

RUN install /tmp/gppy_env.sh /usr/local/bin/gppy_env.sh
RUN install /tmp/gppy_execute /usr/local/bin/gppy_execute
RUN install /tmp/gppy_py /usr/local/bin/gppy_py

# FROM base
# COPY --from=builder /install /usr/local
# COPY src /app
# WORKDIR /app

RUN adduser -D $SERVICE_NAME
# Execute in the host tree
WORKDIR /home/$SERVICE_NAME
RUN mkdir -p Sources
ENV FLACSRCS=/home/$SERVICE_NAME/Sources
RUN mkdir -p Playlists
ENV PLAYLISTS=/home/$SERVICE_NAME/Playlists
RUN chown -R $SERVICE_NAME:$SERVICE_NAME /home/$SERVICE_NAME
USER $SERVICE_NAME
# RUN ls -l /tmp
# RUN ls -l /usr/local/bin

CMD ["ash", "/usr/local/bin/gppy_execute"]
