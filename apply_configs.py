import toml, requests
import subprocess as sbp
from typing import List, Optional, Dict
import os, zipfile, io, gzip, tarfile
import shutil


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


def try_copy(source: str, destination: str) -> None:
    """Try to copy a file, if it can't be found, 
    the error is catched and further manipulation is needed.
    """
    print("Copying config files...")
    try:
        # shutil.copyfile(f"{axioms_dir}/{v}", destination)
        shutil.copy(f"{source}", f"{destination}")
        print("Done!")
    except FileNotFoundError:
        print(f"There is no such directory {destination}, check again.")


def check_if_program(name: str, destination: str, true: str) -> bool:
    """Checks if the name corresponds to the true value, if so,
    is uses the destination for that program for files to be copied.
    """
    if name == true:
        print(f"Configuration files will be copied to {destination}")
        return True
    else:
        print(f"Not {true}, skipping this step...")
        return False


# * Languages
def install_programming_langs(config_file: Dict, basic_command: List) -> None:
    for m in config_file["languages"].values():
        for i in m:
            for k, v in i.items():
                # Create a temporary list to store the full command
                tmp_list = basic_command.copy()
                # tmp_list = "sudo apt install".split(" ")
                tmp_list.append(v)

                # Try first by name
                if k == "name":
                    try:
                        sbp.run(tmp_list, check=True)
                    except sbp.CalledProcessError:
                        print("Not available in repositories or rejected by the user.")
                        print("Trying with the URL.")
                        continue

                # If not, try by url
                if k == "url":
                    download_and_decompress(v)
                # Sometimes, these have scripts
                if k == "script":
                    try:
                        r = sbp.run(v, shell=True, check=True)
                        print(r)
                    except sbp.CalledProcessError:
                        print("Couldn't execute script.")


# * PROGRAMS
def install_programs(config_file: Dict, basic_command: List) -> None:
    for k, v in config_file["programs"].items():
        # * Base programs
        if k == "base":
            sbp.run(basic_command + v)
        # * Special programs
        if k == "special":
            parse_with_url(v, "sudo apt install".split(" "))


# * Shell
def parse_shell(config_file: Dict, axioms_dir: str) -> None:
    # Grab the oh-my-zsh installation script
    omf_file = requests.get(
        "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    )
    # Execute it
    sbp.run(["sh", "-c", omf_file.text])
    # Rewrite zshrc
    zsh_location = f"{os.getenv('HOME')}/.zshrc"
    with open(zsh_location, "w") as z:
        print("Rewriting .zshrc...")
        for k, v in config_file["shell"].items():
            if k == "name":
                print(f"# This is a config file for the {v} shell.\n", file=z)
            if k == "config":
                print("# Global configuration file", file=z)
                print(f"source {v}\n", file=z)
            if k == "alias":
                print("# Aliases file", file=z)
                print(f"source {v}", file=z)
        print("Done!")
    # Deal with the multiplexer
    for k, v in config_file["shell"]["multiplexer"].items():
        print("Copying the multiplexer configuration files")
        destination = f"{os.getenv('HOME')}/.tmux.conf"
        if k == "config":
            try_copy(f"{axioms_dir}/{v}", destination)
        print("Done!")


# * Github configuration
def git_configuration(config_file: Dict, axioms_dir: str) -> None:
    for k, v in config_file["github"].items():
        destination = f"{os.getenv('HOME')}/.gitconfig"
        if k == "file":
            try_copy(f"{axioms_dir}/{v}", destination)


# * Visual Studio Code
def parse_editor(config_file: Dict, axioms_dir: str) -> None:
    for k, v in config_file["editor"].items():
        # First, check to see if the editor is VSCode
        destination = f"{os.getenv('HOME')}/.config/Code/User/"
        if k == "name":
            if is_program := check_if_program(v, destination, "Visual Studio Code"):
                continue
            else:
                break
        # Next, install the respective extensions
        if k == "extensions":
            print("Installing extensions...")
            # Read the extensions file from the repo
            ext_file = toml.load(f"{axioms_dir}/{v}")
            # Look for the extensions section and loop over
            for m, n in ext_file["extensions"].items():
                if m == "names":
                    install_command = "code --install-extension".split(" ")
                    # The extensions are a list to loop over
                    for e in n:
                        tmp_list = install_command.copy()
                        tmp_list.append(e)
                        # Do not prompt for approval
                        tmp_list.append("--force")
                        sbp.run(tmp_list)
            print("Done!")
        # Finally, copy the specified configurations
        if k == "settings":
            try_copy(f"{axioms_dir}/{v}", destination)


# * Terminal
def config_terminal(config_file: Dict, axioms_dir: str) -> None:
    for k, v in config_file["terminal"].items():
        destination = f"{os.getenv('HOME')}/.config/alacritty/"
        if k == "name":
            if is_program := check_if_program(v, destination, "Alacritty"):
                continue
            else:
                break
        if k == "config":
            try_copy(f"{axioms_dir}/{v}", destination)
