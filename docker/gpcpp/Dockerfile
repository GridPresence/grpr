#
# Copyright TLM Partners, Inc. All Rights Reserved
#
# Use an LTS image for the base
FROM ubuntu:24.04 as base

FROM base as builder
ENV SERVICE_NAME="gpcpp"
ENV PIP_ROOT_USER_ACTION=ignore

# Non-interactive apt tools behaviour
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -y; \
    apt-get upgrade -y; \
    apt-get install -y bash \
    build-essential \ 
    ca-certificates \
    curl \
    gnupg2 \
    wget \
    jq \ 
    openssh-client \
    python3-pip \
    software-properties-common \
    zip \
    dos2unix \
    g++ \
    libcpprest-dev \
    libboost-all-dev \
    libssl-dev \
    cmake

    # apt-get -qqy install build-essential ca-certificates bash curl docker.io gnupg2 wget jq \ 
    # openssh-client python3-pip software-properties-common zip dos2unix

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN python3 -m pip install --break-system-packages --upgrade -r /requirements.txt
# FROM base
# COPY --from=builder /install /usr/local
# COPY src /app
# WORKDIR /app

