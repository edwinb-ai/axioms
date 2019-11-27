#!/usr/bin/env bash

# Update everything from the start
sudo apt update;
# Install git
sudo apt install git -y;

# Create a directory to store everything
mkdir $HOME/programs/;
cd $HOME/programs/;
# Clone the axioms directory from GitHub
git clone https://github.com/edwinb-ai/axioms.git
# Save the axioms directory for later
cd axioms
AXIOMSDIR=$(pwd)

# Install anaconda
echo "Installing Anaconda distribution"
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh;
bash Anaconda3-2019.10-Linux-x86_64.sh;

# Save the binary directory for later
ANACONDABIN="$HOME/anaconda3/bin/";

# Create a new environment and activate it
ANACONDAENV="toml";
echo "Creating the $ANACONDAENV environment.";
# Change location to the conda directory
cd $ANACONDABIN
./conda create -n $ANACONDAENV python=3 --yes;
# Use source for now because the shell is not yet configured
source activate $ANACONDAENV;
echo "$ANACONDAENV environment created and activated!";

# In the new environment, install the necessary packages
echo "Installing Python packages for the installation";
pip install poetry;
echo "Done!";

# Now, change back to the axioms directory
cd $AXIOMSDIR

# Run each task separately
echo "Installing programming languages...";
poetry run invoke languages;
echo "Installing programs...";
poetry run invoke programs;
echo "Configuring shell...";
poetry run invoke shell;
echo "Adding git configuration...";
poetry run invoke git;
echo "Configuring terminal...";
poetry run invoke terminal;
echo "Done!";

# Finally, remove the environment
echo "Removing the $ANACONDAENV environment.";
$ANACONDABIN/conda remove -n $ANACONDAENV --all --yes;
echo "DONE! :) Rebooting might be necessary.";
