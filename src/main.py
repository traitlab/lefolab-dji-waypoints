
from pydantic import ValidationError

from lib.build_template_kml import BuildTemplateKML
from lib.build_waylines_wpml import BuildWaylinesWPML
from lib.extractpoints import ExtractPoints

try:
    pipeline = ExtractPoints()
    pipeline.load()
    pipeline.setup()
    pipeline.get_points_elevation_from_dsm()
    pipeline.reproject("epsg:32618", "epsg:32618")
    pipeline.write_global_csv()
    pipeline.write_waypoint_csv()

    build_template_kml = BuildTemplateKML()
    build_template_kml.setup()
    build_template_kml.addNewPlacemark()
    build_template_kml.saveNewKML()

    build_waylines_wpml = BuildWaylinesWPML()
    build_waylines_wpml.setup()
    build_waylines_wpml.addNewPlacemark()
    build_waylines_wpml.saveNewWPML()

except ValidationError as e:
    print(f"Configuration error: {e}")
