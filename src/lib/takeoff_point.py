import geopandas as gpd
import pyproj
from shapely.geometry import Point

from lib.config import config


class TakeOffPoint():
    def __init__(self):
        self.lat_y = None
        self.lon_x = None
        self.target_epsg = None
        self.target_crs = None
        self.geometry = None

    def setup(self):

        coords = config.takeoff_point_wgs84_global_laty_lonx.split(", ")
        self.lat_y = float(coords[0])
        self.lon_x = float(coords[1])
        self.target_epsg = config.from_epsg.upper()

    def reproject(self):
        # Convert the coordinates to the target EPSG
        wgs84 = pyproj.CRS('EPSG:4326')
        self.target_crs = pyproj.CRS(self.target_epsg)

        project = pyproj.Transformer.from_crs(
            wgs84, self.target_crs, always_xy=True)
        x, y = project.transform(self.lon_x, self.lat_y)

        # Create a GeoDataFrame
        self.geometry = [Point(x, y)]

    def save(self):
        gdf = gpd.GeoDataFrame(geometry=self.geometry, crs=self.target_crs)

        # Save to GeoPackage
        gdf.to_file(config.takeoff_point_file_path,
                    layer='takeoff_point_layer', driver='GPKG')
