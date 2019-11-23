import toml, requests
import subprocess as sbp
from typing import List, Optional
import os, zipfile, io, gzip, tarfile
import shlex


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


def download_and_decompress(url: str) -> None:
    """Download a zip or tar gzip file with its URL and
    decompress it in the current working directory.
    """
    if "zip" in url:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            print("Downloading the file...")
            print("Extracting the file...")
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()
            print("Done!")
        else:
            raise requests.HTTPError("Could not download the file!")

    elif ".tar.gz" in url:
        r = requests.get(url, stream=True)
        if r.status_code == requests.codes.ok:
            print("Downloading the file...")
            print("Extracting the file...")
            with gzip.open(r.raw) as g:
                t = tarfile.TarFile(fileobj=g)
                t.extractall()
            print("Done!")
        else:
            raise requests.HTTPError("Could not download the file!")

    else:
        raise Exception("Couldn't handle the file, no method available for it.")


def parse_with_url(programs: List[str], command: List[str]) -> None:
    """Take in a list of strings and a command in list form,
    and traverse it.
    
    It will try to apply the command to every program in the list,
    if it fails, it will try to use its URL to download it from the
    internet.

    In case it's a git repository, it will only clone it. If it's a
    compressed file, it will download it and decompress it.
    """
    for p in programs:
        for k, v in p.items():
            # Create a temporary list to store the full command
            tmp_list = command.copy()
            tmp_list.append(v)
            print(f"searching for {v}")
            if k == "name":
                try:
                    sbp.run(tmp_list, check=True)
                except sbp.CalledProcessError:
                    print("Not available in repositories or rejected by the user.")
                    print("Trying with the URL.")
                    continue
            if k == "url":
                if ".git" in v:
                    # The command is different now, we must clone each repo
                    tmp_list = "git clone".split(" ")
                    tmp_list.append(v)
                    try:
                        print("Trying to clone the following repository...")
                        print(f"{tmp_list}")
                        sbp.run(tmp_list, check=True)
                        print("Done!")
                    except sbp.CalledProcessError:
                        print("Could not clone the repository.")
                # If the files are compressed, download and decompress
                download_and_decompress(v)


# * Begin parsing
# Load the configuration file and save it as a dictionary
config_file = toml.load("master-config.toml")

# Master command to install most things
basic_command = ["sudo", "eopkg", "it"]

# Save the axioms directory
axioms_dir = os.getcwd()

# First, create a special directory to store everything
# and change the current directory to it
create_programs_dir()
os.chdir(f"{os.getenv('HOME')}/programs")

# * Languages
# for m in config_file["languages"].values():
#     for i in m:
#         for k, v in i.items():
#             # Create a temporary list to store the full command
#             tmp_list = basic_command.copy()
#             # tmp_list = "sudo apt install".split(" ")
#             tmp_list.append(v)

#             # Try first by name
#             if k == "name":
#                 try:
#                     sbp.run(tmp_list, check=True)
#                 except sbp.CalledProcessError:
#                     print("Not available in repositories or rejected by the user.")
#                     print("Trying with the URL.")
#                     continue

#             # If not, try by url
#             if k == "url":
#                 download_and_decompress(v)
#             # Sometimes, these have scripts
#             if k == "script":
#                 try:
#                     r = sbp.run(v, shell=True, check=True)
#                     print(r)
#                 except sbp.CalledProcessError:
#                     print("Couldn't execute script.")

# * PROGRAMS
# for k, v in config_file["programs"].items():
#     # * Base programs
#     if k == "base":
#         sbp.run(basic_command + v)
#     # * Special programs
#     if k == "special":
#         parse_with_url(v, "sudo apt install".split(" "))

# * Shell
# Grab the oh-my-zsh installation script
# omf_file = requests.get(
#     "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
# )
# # Execute it
# sbp.run(["sh", "-c", omf_file.text])
# Rewrite zshrc
zsh_location = f"{os.getenv('HOME')}/.testrc"
with open(zsh_location, "w") as z:
    for k, v in config_file["shell"].items():
        if k == "name":
            print(f"# This is a config file for the {v} shell.\n", file=z)
        if k == "config":
            print("# Global configuration file", file=z)
            print(f"source {v}\n", file=z)
        if k == "alias":
            print("# Aliases file", file=z)
            print(f"source {v}\n", file=z)

