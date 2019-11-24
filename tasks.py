from invoke import task
from apply_configs import parse_editor, create_programs_dir, git_configuration
from apply_configs import config_terminal, install_programming_langs
from apply_configs import install_programs, parse_shell
import toml, os


# * Begin parsing
def setup():
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

    return config_file, basic_command, axioms_dir


# * Languages
@task
def languages(c):
    config_file, basic_command, _ = setup()
    install_programming_langs(config_file, basic_command)


# * Progams
@task
def progams(c):
    config_file, basic_command, _ = setup()
    install_programs(config_file, basic_command)


# * Shell
@task
def shell(c):
    config_file, _, axioms_dir = setup()
    parse_shell(config_file, axioms_dir)


# * Editor
@task
def editor(c):
    config_file, _, axioms_dir = setup()
    parse_editor(config_file, axioms_dir)


# * GitHub config
@task
def git(c):
    config_file, _, axioms_dir = setup()
    git_configuration(config_file, axioms_dir)


# * Terminal
@task
def terminal(c):
    config_file, _, axioms_dir = setup()
    config_terminal(config_file, axioms_dir)


# * Just a test task
@task
def test(c):
    print("Just testing")

