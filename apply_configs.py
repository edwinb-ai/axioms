import toml
import subprocess as sbp
import requests
from typing import List, Optional
import os, zipfile, io


def create_programs_dir(name: Optional[str] = "programs") -> None:
    """Try to create a special directory to store most of the programs
    and utilities needed.
    """
    try:
        programs_dir = f"{os.getenv('HOME')}/{name}"
        print(f"Trying to create the following directory {programs_dir}")
        os.mkdir(programs_dir)
        print(f"Successfully created!")
    except FileExistsError:
        print("Because the directory exists, nothing will be done.")
        pass


def parse_special_programs(programs: List, command: List):
    # First, create a special directory to store everything
    create_programs_dir()
    os.chdir(f"{os.getenv('HOME')}/programs")

    # Then, traverse the list with the programs
    for p in programs:
        for k, v in p.items():
            tmp_list = command.copy()
            tmp_list.append(v)
            print(f"searching for {v}")
            if k == "name":
                try:
                    sbp.run(tmp_list, check=True)
                except sbp.CalledProcessError:
                    print("Not available in repositories, trying with url")
                    continue
            if k == "url":
                if ".git" in v:
                    tmp_list = "git clone".split(" ")
                    tmp_list.append(v)
                    try:
                        print("Trying to clone the repository...")
                        sbp.run(tmp_list, check=True)
                        print("Done!")
                    except sbp.CalledProcessError:
                        print("Could not clone the repository")
                if "zip" in v:
                    r = requests.get(v)
                    if r.status_code == requests.codes.ok:
                        print("Downloading the file...")
                        print("Extracting the file...")
                        z = zipfile.ZipFile(io.BytesIO(r.content))
                        z.extractall()
                        print("Done!")
                    else:
                        raise requests.HTTPError("Could not download the file!")
                if ".tar" in v:
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
        parse_special_programs(v, "sudo apt install".split(" "))

# * Shell
# Grab the oh-my-zsh installation script
# omf_file = requests.get(
#     "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
# )
# # Execute it
# sbp.run(["sh", "-c", omf_file.text])
# TODO: Parse the TOML file once oh-my-fish has been installed
