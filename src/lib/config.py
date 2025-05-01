import argparse
import os
import sys
from pathlib import Path

import yaml

from model.config import Config


# -----------------------------------------------------------------------------
def load_config(config_path: str) -> Config:
    # Load the configuration file
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        return Config(**config_data)
    else:
        print(f"Configuration file not found: {config_path}")
        sys.exit(1)


# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Generate the KMZ from a list of coordinates (lat, lon, elevation) in a CSV file.')
parser.add_argument('--config', '-s', type=str, required=False,
                    help='Path to the configuration file. Other choice is to provide the --csv option.')
parser.add_argument('--csv', '-c', type=str, required=False,
                    help='Path to the input CSV file containing waypoints. Other choice is to provide the --config option.')
parser.add_argument('--output', '-o', type=str, default='./output',
                    help='Output directory path (default: ./output)')
parser.add_argument('--approach', '-a', type=float, default=10,
                    help='Approach above the tree crown in meters (default: 10)')
parser.add_argument('--buffer', '-b', type=float, default=6,
                    help='Buffer above the tree crown in meters (default: 6)')
parser.add_argument('--debug', '-d', action='store_true',
                    help='Run in debug mode (default: False)')

args = parser.parse_args()

# Validate that either --config or --csv is provided
if not args.config and not args.csv:
    parser.error("Either --config or --csv must be provided")
    sys.exit(1)

# Create config object
if args.config:
    config = load_config(args.config)
    config.debug_mode = args.debug
else:
    # Get base_name from CSV file path
    base_name = Path(args.csv).stem  # Get filename without extension
    
    # Create a default Config object with command line values
    config = Config(
        approach=args.approach,
        buffer=args.buffer,
        base_path=args.output,
        base_name=base_name,
        points_csv_file_path=args.csv,
        debug_mode=args.debug
    )
