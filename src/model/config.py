from pathlib import Path

import yaml
from pydantic import BaseModel, FilePath, ValidationError


class Config(BaseModel):
    tree_polygons_file_path: FilePath
    tree_polygons_layer: str

    starting_point_file_path: FilePath
    starting_point_layer: str

    zone_of_interest_path: FilePath
    zone_of_interest_layer: str

    dsm_file_path: FilePath

    global_csv_file_path: Path
    points_csv_file_path: Path

    num_waypoints_per_cluster: int

    kml_model_file_path: FilePath
    output_kml_file_path: Path

    wpml_model_file_path: FilePath
    output_wpml_file_path: Path

    class Config:
        arbitrary_types_allowed = True
