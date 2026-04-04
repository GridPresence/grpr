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

RUN mkdir -p /tmp/gpm
COPY installs/gpm/* /tmp/gpm
COPY installs/* /tmp

RUN python3 -m pip install --break-system-packages --upgrade -r /tmp/reqs-playgen.txt

RUN mkdir -p /usr/local/bin/gpm
RUN install /tmp/gpm/__init__.py /usr/local/bin/gpm/__init__.py
RUN install /tmp/gpm/audio.py /usr/local/bin/gpm/audio.py
RUN install /tmp/gpm/db.py /usr/local/bin/gpm/db.py
RUN install /tmp/gpm/extract.py /usr/local/bin/gpm/extract.py

RUN install /tmp/gppy_env.sh /usr/local/bin/gppy_env.sh

RUN install /tmp/gppy_playgen /usr/local/bin/gppy_playgen
RUN install /tmp/gppy_exec_playgen /usr/local/bin/gppy_exec_playgen


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

CMD ["ash", "/usr/local/bin/gppy_exec_playgen"]
