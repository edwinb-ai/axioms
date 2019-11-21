#!/usr/bin/env zsh

# Install anaconda
echo "Installing Anaconda distribution"
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh;
bash Anaconda3-2019.10-Linux-x86_64.sh;

# Change to the directory
cd $HOME/anaconda3/bin/
echo "Now in the $(pwd) directory."

# Create a new environment and activate it
ANACONDAENV="toml";
echo "Creating the $ANACONDAENV environment."
./conda create -n $ANACONDAENV python=3
./conda activate $ANACONDAENV

# In the new environment, install a TOML parser
pip install tomlkit

# And run the configuration script
python apply_configs.py

echo "DONE! :)"