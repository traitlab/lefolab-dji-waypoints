import os
import sys

import yaml

from model.config import Config


def load_config() -> Config:
    # Define the paths for dev and prod modes
    config_path = os.path.join('./config/settings.yaml')
    prod_path = "/usr/local/etc/lefolab_drone_src/settings.yaml"

    # Load the configuration file
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        return Config(**config_data)
    else:
        if os.path.exists(prod_path):
            with open(prod_path, 'r') as file:
                config_data = yaml.safe_load(file)
            return Config(**config_data)
        else:
            print(
                f"Configuration file not found: {prod_path}")
            sys.exit(1)  # Exit the program with a non-zero status


# Usage
config = load_config()
