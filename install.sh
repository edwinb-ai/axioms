#!/usr/bin/env bash

# Update everything from the start
sudo apt update;

PROGRAMSDIR=$HOME/programs/
# Save the axioms directory for later
cd $PROGRAMSDIR/axioms/
AXIOMSDIR=$(pwd)

# Install pyenv from the repositories
sudo apt install python3-pyenv;

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
poetry install;
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
