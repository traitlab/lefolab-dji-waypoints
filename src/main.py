
from pydantic import ValidationError

from lib.pipeline import Pipeline

try:
    pipeline = Pipeline()
    pipeline.load()
    pipeline.setup()
    pipeline.select_random_points()
    pipeline.sort_points_by_distance_from_starting_point()
    pipeline.get_points_elevation_from_dsm()
    pipeline.reproject()
    pipeline.write_global_csv()
    pipeline.write_waypoint_csv()
except ValidationError as e:
    print(f"Configuration error: {e}")
