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
parser.add_argument('--config', required=False,
                    help='Path to the configuration file')
parser.add_argument('--flight_height', '-fh', type=float, required=False,
                    help='Flight height in meters')
parser.add_argument('--takeoff_point_elevation', '-tpe', type=float, required=False,
                    help='Takeoff point elevation in meters')
parser.add_argument('--point_dsm_height_approach', '-pdha', type=float, default=10,
                    help='Point DSM height approach in meters (default: 10)')
parser.add_argument('--point_dsm_height_buffer', '-pdhb', type=float, default=6,
                    help='Point DSM height buffer in meters (default: 6)')
parser.add_argument('--output', '-o', type=str, default='./output',
                    help='Output directory path (default: ./output)')
parser.add_argument('--csv', '-c', type=str, required=False,
                    help='Path to the input CSV file containing waypoints')
parser.add_argument('--debug', '-d', action='store_true',
                    help='Run in debug mode (default: False)')

args = parser.parse_args()

# Validate that either --config or --csv is provided
if not args.config and not args.csv:
    parser.error("Either --config or --csv must be provided")
    sys.exit(1)

# If --csv is provided, flight_height and takeoff_point_elevation are required
if args.csv and (args.flight_height is None or args.takeoff_point_elevation is None):
    parser.error("When --csv is provided, both --flight_height and --takeoff_point_elevation are required")
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
        flight_height=args.flight_height,
        takeoff_point_elevation=args.takeoff_point_elevation,
        point_dsm_height_approach=args.point_dsm_height_approach,
        point_dsm_height_buffer=args.point_dsm_height_buffer,
        base_path=args.output,
        base_name=base_name,
        points_csv_file_path=args.csv,
        debug_mode=args.debug
    )
