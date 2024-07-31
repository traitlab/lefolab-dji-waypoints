import argparse
import os
import sys

import yaml

from model.config import Config


def load_config(config_path: str) -> Config:
    # Load the configuration file
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        return Config(**config_data)
    else:
        print(f"Configuration file not found: {config_path}")
        sys.exit(1)  # Exit the program with a non-zero status


# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Generate the KMZ from a list of coordinates (lat, lon, elevation) in a CSV file.')
parser.add_argument('--config', required=True,
                    help='Path to the configuration file')

args = parser.parse_args()

# Usage
config = load_config(args.config)
