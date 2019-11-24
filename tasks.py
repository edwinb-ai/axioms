from invoke import task
from apply_configs import parse_editor, create_programs_dir
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


@task
def editor(c):
    config_file, basic_command, axioms_dir = setup()
    parse_editor(config_file, axioms_dir)
