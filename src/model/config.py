import re
from pathlib import Path

from pydantic import BaseModel, Field, FilePath, field_validator
from typing_extensions import Annotated


class Config(BaseModel):
    flight_height: int
    takeoff_point_elevation: int
    point_dsm_height_approach: int
    point_dsm_height_buffer: int

    global_csv_file_path: Path
    points_csv_file_path: Path
    shortest_path_csv_file_path: Path

    kml_model_file_path: FilePath
    output_kml_file_path: Path

    wpml_model_file_path: FilePath
    output_wpml_file_path: Path

    kmz_base_name: str
    kmz_root_file_path: Path

    class Config:
        arbitrary_types_allowed = True

    @field_validator('takeoff_point_wgs84_global_laty_lonx')
    def validate_coords(cls, v):
        try:
            lat, lon = map(float, v.split(','))
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError
        except ValueError:
            raise ValueError(
                'Invalid coordinates. Should be in the format "latitude, longitude" with valid ranges.')
        return v

    @field_validator('from_epsg', 'to_epsg')
    def validate_epsg(cls, v):
        if not re.match(r'^epsg:\d+$', v, re.IGNORECASE):
            raise ValueError('EPSG code must be in the format "epsg:XXXX"')
        return v
