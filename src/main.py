
from pydantic import ValidationError

from lib.build_template_kml import BuildTemplateKML
from lib.build_waylines_wpml import BuildWaylinesWPML
from lib.create_kmz import CreateKMZ
from lib.extract_points import ExtractPoints

try:
    extract_points = ExtractPoints()
    extract_points.load()
    extract_points.setup()
    extract_points.get_points_elevation_from_dsm()
    extract_points.reproject("epsg:32618", "epsg:32618")
    extract_points.write_global_csv()
    extract_points.write_waypoint_csv()

    build_template_kml = BuildTemplateKML()
    build_template_kml.setup()
    build_template_kml.addNewPlacemark()
    build_template_kml.saveNewKML()

    build_waylines_wpml = BuildWaylinesWPML()
    build_waylines_wpml.setup()
    build_waylines_wpml.addNewPlacemark()
    build_waylines_wpml.saveNewWPML()

    create_kmz = CreateKMZ()
    create_kmz.create_kmz()

except ValidationError as e:
    print(f"Configuration error: {e}")
