import toml
import subprocess as sbp
import requests
from typing import List, Optional
import os


def create_programs_dir(name: Optional[str] = "programs") -> None:
    """Try to create a special directory to store most of the programs
    and utilities needed.
    """
    try:
        os.mkdir(os.environ(["HOME"]) + f"/{name}")
    except FileExistsError:
        print("Because the directory exists, nothing will be done.")
        pass


def parse_special_programs(programs: List, command: List):
    pass


# Load the configuration file and save it as a dictionary
config_file = toml.load("master-config.toml")

# * PROGRAMS
basic_command = ["sudo", "eopkg", "it"]

# Start parsing the programs section
for k, v in config_file["programs"].items():
    # * Base programs
    if k == "base":
        # sbp.run(basic_command + v)
        pass
    # * Special programs
    if k == "special":
        print(v)
        parse_special_programs(v)

    # TODO: Deal with the installation of flatpak packages

# * Shell
# Grab the oh-my-zsh installation script
# omf_file = requests.get(
#     "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
# )
# # Execute it
# sbp.run(["sh", "-c", omf_file.text])
# TODO: Parse the TOML file once oh-my-fish has been installed
