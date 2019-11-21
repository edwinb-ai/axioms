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

# * Shell

sbp.run(["sh", "-c"])
