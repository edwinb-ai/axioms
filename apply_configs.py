import toml
import subprocess as sbp


# Load the configuration file and save it as a dictionary
config_file = toml.load("master-config.toml")

# ==== PROGRAMS ==== #
basic_command = ["sudo", "eopkg", "it"]
for k, v in config_file["programs"].items():
    if k == "base":
        sbp.run(basic_command + v)
