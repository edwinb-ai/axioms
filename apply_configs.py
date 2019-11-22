import toml
import subprocess as sbp
import requests


# Load the configuration file and save it as a dictionary
config_file = toml.load("master-config.toml")

# * Programs
basic_command = ["sudo", "eopkg", "it"]
for k, v in config_file["programs"].items():
    if k == "base":
        sbp.run(basic_command + v)
    # TODO: Deal with the special programs

# * Shell
# Grab the oh-my-zsh installation script
omf_file = requests.get(
    "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
)
# Execute it
sbp.run(["sh", "-c", omf_file.text])
# TODO: Parse the TOML file once oh-my-fish has been installed
