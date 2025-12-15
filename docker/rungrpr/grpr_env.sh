#!/usr/bin/env bash
echo "Setting up the $HOME environment"
# Set things up to allow the use of JFrog virtual PyPi repo
mkdir -p $HOME/.pip
# Fix things up for a local pip configuration
# to avoid warnings for non-root installs in the container
mkdir -p $HOME/.local
mkdir -p $HOME/.local/bin
export PATH=$HOME/.local/bin:$PATH
# This bootstraps access to the TLM PyPi repository to allow installations
export JFPYPI="index-url = https://$JFROG_USER:$JFROG_TOKEN@$JFROG_URL/artifactory/api/pypi/pypi/simple"
echo "[global]" > $HOME/.pip/pip.conf
echo $JFPYPI >> $HOME/.pip/pip.conf
# Allow upload publication of Python modules
#cp $HOME/credentials/pypirc $HOME/.pypirc
#. $HOME/credentials/aws.conf
# Configure JFrog credentials
#export JF_API_KEY=$(cat $HOME/credentials/jfrog-iac_service-token)
#export JF_AF_URL="https://artifactory.tlmpartners.com/"
#export JF_USER="iac_service"
#export JF_PASSWD="APAJNYYr9peNV7Y43eS9MhmVH7b"
export TF_TOKEN_artifactory_tlmpartners_com=$JFROG_TOKEN
export CI="true"
printenv | sort
