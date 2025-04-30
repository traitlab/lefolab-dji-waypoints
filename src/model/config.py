import re
from pathlib import Path

from pydantic import BaseModel, Field, FilePath, field_validator
from typing_extensions import Annotated

# config
# base_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize'
# base_name: '20240529_sblz1z2_p1'

# # global_csv_file_path: 'global_values.csv'
# # points_csv_file_path: 'waypoints.csv'
# # shortest_path_csv_file_path: 'waypoints_shortest_path.csv'

# kml_model_file_path: './scripts/wpml/model/Waypoint2/wpmz/template.kml'
# # output_kml_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/wpmz/template.kml'

# wpml_model_file_path: 'scripts/wpml/model/Waypoint2/wpmz/waylines.wpml'
# # output_wpml_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/wpmz/waylines.wpml'

# # kmz_base_name: '20240529_sblz1z2_p1'
# # kmz_base_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize'


class Config(BaseModel):
    flight_height: int
    takeoff_point_elevation: int
    point_dsm_height_approach: int
    point_dsm_height_buffer: int

    base_path: Path
    base_name: str

    points_csv_file_path: FilePath

    kml_model_file_path: FilePath = './scripts/wpml/model/Waypoint3_modif/wpmz/template.kml'
    output_kml_file_path: Path = 'wpmz/template.kml'
    wpml_model_file_path: FilePath = './scripts/wpml/model/Waypoint3_modif/wpmz/waylines.wpml'
    output_wpml_file_path: Path = 'wpmz/waylines.wpml'

    waylines_placemark_no_action: FilePath = './config/waylines_placemark_no_action.json'
    waylines_placemark_with_actions: FilePath = './config/waylines_placemark_with_actions.json'

    debug_mode: bool = False

    class Config:
        arbitrary_types_allowed = True
