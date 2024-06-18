from pathlib import Path

from pydantic import BaseModel, FilePath


class Config(BaseModel):
    tree_polygons_file_path: FilePath
    starting_point_file_path: FilePath
    zone_of_interest_path: FilePath
    dsm_file_path: FilePath

    base_height_ortho: int

    from_epsg: str
    to_epsg: str

    global_csv_file_path: Path
    points_csv_file_path: Path

    num_waypoints_per_cluster: int

    kml_model_file_path: FilePath
    output_kml_file_path: Path

    wpml_model_file_path: FilePath
    output_wpml_file_path: Path

    kmz_base_name: str
    kmz_root_file_path: Path

    class Config:
        arbitrary_types_allowed = True
