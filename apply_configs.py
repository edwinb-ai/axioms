import toml


config_file = toml.load("master-config.toml")
print(config_file)
