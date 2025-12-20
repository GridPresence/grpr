echo "Setting up the $HOME environment"
# Set things up to allow the use of JFrog virtual PyPi repo
mkdir -p $HOME/.pip
# Fix things up for a local pip configuration
# to avoid warnings for non-root installs in the container
mkdir -p $HOME/.local
mkdir -p $HOME/.local/bin
export PATH=$HOME/.local/bin:$PATH
#export CI="true"
printenv | sort
