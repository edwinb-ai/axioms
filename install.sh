#!/usr/bin/env bash

# Create a directory to store everything
mkdir $HOME/programs/
cd $HOME/programs/

# Install anaconda
echo "Installing Anaconda distribution"
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh;
bash Anaconda3-2019.10-Linux-x86_64.sh;

# Save the binary directory for later
ANACONDABIN="$HOME/anaconda3/bin";

# Create a new environment and activate it
ANACONDAENV="toml";
echo "Creating the $ANACONDAENV environment.";
$ANACONDABIN/conda create -n $ANACONDAENV python=3 --yes;
$ANACONDABIN/conda activate $ANACONDAENV;
echo "$ANACONDAENV environment created!";

# In the new environment, install the necessary packages
echo "Installing Python packages for the installation";
pip install toml requests invoke
echo "Done!";

# Run each task separately
echo "Installing programming languages...";
invoke languages
echo "Installing programs...";
invoke programs
echo "Configuring shell...";
invoke shell
echo "Configuring editor...";
invoke editor
echo "Adding git configuration...";
invoke git
echo "Configuring terminal...";
invoke terminal
echo "Done!";

# Finally, remove the environment
echo "Removing the $ANACONDAENV environment.";
$ANACONDABIN/conda remove -n $ANACONDAENV --all --yes;
echo "DONE! :) Rebooting might be necessary.";
