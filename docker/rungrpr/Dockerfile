#
# Copyright TLM Partners, Inc. All Rights Reserved
#
# Use an LTS image for the base
FROM ubuntu:24.04 as rungrpr
ENV SERVICE_NAME="rungrpr"
# Repairing the Ubuntu default shell as bash
RUN rm /bin/sh ; \
    ln -s /bin/bash /bin/sh
# Non-interactive apt tools behaviour
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get -qqy update; \
    apt-get -qqy upgrade; \
    apt-get -qqy install build-essential ca-certificates bash curl docker.io gnupg2 wget jq \ 
    openssh-client python3-pip software-properties-common zip dos2unix
# Install the HashiCorp GPG key
# RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
#     gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
# RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
#     https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list
# Install the latest Terraform and Packer applications
# RUN apt-get -qqy update; \
#     apt-get -qqy install terraform packer
# Clean some space
RUN apt-get -qqy autoclean
# Add some python dependencies
ENV PIP_ROOT_USER_ACTION=ignore
# RUN python3 -m pip install --upgrade --break-system-packages pip 
RUN python3 -m pip install --break-system-packages --upgrade \
    build twine tbump truststore sphinx sphinx-autodoc-typehints \
    sphinxcontrib-napoleon sphinx_rtd_theme boto3 botocore pytest \
    moto[all] typer[all] dohq-artifactory black mypy pylint packaging
# Install executables for this image
COPY grpr_execute /tmp/grpr_execute
RUN install /tmp/grpr_execute /usr/local/bin/grpr_execute
COPY grpr_env.sh /tmp/grpr_env.sh
RUN install /tmp/grpr_env.sh /usr/local/bin/grpr_env.sh
COPY grpr_python /tmp/grpr_python
RUN install /tmp/grpr_python /usr/local/bin/grpr_python
# Set up a non-root user
RUN useradd -m $SERVICE_NAME
# Create host FS mount points
#RUN mkdir -p /home/$SERVICE_NAME/credentials /home/$SERVICE_NAME/work
RUN mkdir -p /home/$SERVICE_NAME/work
# Execute in the host tree
WORKDIR /home/$SERVICE_NAME/work
RUN chown -R $SERVICE_NAME:$SERVICE_NAME /home/$SERVICE_NAME
USER $SERVICE_NAME

CMD ["bash", "grpr_execute"]
