import toml
import subprocess as sbp
import requests


# Load the configuration file and save it as a dictionary
config_file = toml.load("master-config.toml")

# * PROGRAMS
basic_command = ["sudo", "eopkg", "it"]

# Start parsing the programs section
for k, v in config_file["programs"].items():
    # * Base programs
    if k == "base":
        sbp.run(basic_command + v)
    # TODO: Deal with the special programs
    # TODO: Deal with the installation of flatpak packages

# * Shell
# Grab the oh-my-zsh installation script
omf_file = requests.get(
    "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
)
# Execute it
sbp.run(["sh", "-c", omf_file.text])
# TODO: Parse the TOML file once oh-my-fish has been installed
