#!/usr/bin/env zsh

# Install anaconda
echo "Installing Anaconda distribution"
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh;
bash Anaconda3-2019.10-Linux-x86_64.sh;

# Save the binary directory for later
ANACONDABIN="$HOME/anaconda3/bin"

# Create a new environment and activate it
ANACONDAENV="toml";
echo "Creating the $ANACONDAENV environment."
$ANACONDABIN/conda create -n $ANACONDAENV python=3 --yes
$ANACONDABIN/conda activate $ANACONDAENV

# In the new environment, install a TOML parser
pip install toml

# And run the configuration script
python apply_configs.py

# Finally, remove the environment
$ANACONDABIN/conda remove -n $ANACONDAENV --all --yes
echo "Removing the $ANACONDAENV environment."

echo "DONE! :) Rebooting is necessary now."