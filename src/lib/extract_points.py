import csv

import geopandas as gpd
import rasterio
from pyproj import Transformer

from lib.config import config


class ExtractPoints:
    def __init__(self):
        self.zone_of_interest_gdf = None
        self.starting_point_gdf = None
        self.trees_gdf = None
        self.trees_in_zone_gdf = None
        self.clusters = None
        self.top_polygons_per_cluster = None
        self.epsg_code = None
        self.random_points = []
        self.sorted_points = None
        self.points_elevation = None
        self.starting_point_elevation = None
        self.sorted_points_transformed = None
        self.starting_point_transformed = None

    # Function to read zone of interest GeoDataFrame
    def read_zone_of_interest_gdf(self):
        try:
            self.zone_of_interest_gdf = gpd.read_file(
                config.zone_of_interest_path)
        except ValueError as e:
            # Log error
            print(f"Error reading GeoDataFrame: {e}")

    def load(self):
        # Load the starting point and clusters layers from GeoPackage
        self.starting_point_gdf = gpd.read_file(
            config.starting_point_file_path)
        self.trees_gdf = gpd.read_file(config.tree_polygons_file_path)

        try:
            self.read_zone_of_interest_gdf()
            self.trees_in_zone_gdf = gpd.overlay(
                self.trees_gdf, self.zone_of_interest_gdf, how='intersection')
        except Exception:
            self.trees_in_zone_gdf = self.trees_gdf

        # Load the DSM raster data
        self.dsm_dataset = rasterio.open(config.dsm_file_path)

    # Function to calculate distance between two points
    @staticmethod
    def calculate_distance(point1, point2):
        return point1.distance(point2)

    # Function to get elevation from DSM
    @staticmethod
    def get_elevation_from_dsm(point, dataset):
        coords = [(point.x, point.y)]
        for val in dataset.sample(coords):
            return val[0]

    # Define a function to select the top polygons per cluster based on area and distance to starting point
    def select_top_polygons(self, group):
        # Sort polygons by distance to the starting point
        sorted_polygons = group.sort_values(by='distance_to_start')

        # Select the 5 polygons with the greatest area among the closest ones
        top_polygons = sorted_polygons.nlargest(5, 'Shape_Area')

        return top_polygons

    def setup(self):
        self.starting_point = self.starting_point_gdf.geometry.iloc[0]

        # Calculate the centroid for each tree polygon
        self.trees_in_zone_gdf['centroid'] = self.trees_in_zone_gdf.geometry.centroid
        # self.trees_in_zone_gdf['area'] = self.trees_in_zone_gdf.area
        self.trees_in_zone_gdf['distance_to_start'] = self.trees_in_zone_gdf['centroid'].distance(
            self.starting_point)

        # Group trees by cluster_id
        self.clusters = self.trees_in_zone_gdf.groupby('cluster_id')

        # Apply the function to each group
        self.top_polygons_per_cluster = self.clusters.apply(
            self.select_top_polygons)

        # Reset index
        self.top_polygons_per_cluster.reset_index(drop=True, inplace=True)

        # # Sort each group by area attribute and select top 5 polygons
        # self.top_polygons_per_cluster = self.clusters.apply(
        #     lambda x: x.nlargest(5, 'area')).reset_index(drop=True)

        # Extract EPSG code
        self.epsg_code = self.trees_in_zone_gdf.crs.to_epsg()

    def get_points_elevation_from_dsm(self):
        self.points_elevation = []
        # Iterate over each cluster
        for _, cluster_polygons in self.top_polygons_per_cluster.groupby('cluster_id'):
            # Extract elevations for polygons in the cluster
            cluster_elevations = [self.get_elevation_from_dsm(
                point, self.dsm_dataset) + 10 for point in cluster_polygons['centroid']]
            self.points_elevation.extend(cluster_elevations)

        # Calculate elevation of the starting point once
        self.starting_point_elevation = self.get_elevation_from_dsm(
            self.starting_point, self.dsm_dataset)

    def reproject(self, epsg_from, epsg_to):
        # Transform coordinates
        transformer = Transformer.from_crs(epsg_from, epsg_to)
        self.sorted_points_transformed = [transformer.transform(
            point.x, point.y) for point in self.top_polygons_per_cluster['centroid']]
        self.starting_point_transformed = transformer.transform(
            self.starting_point.x, self.starting_point.y)

    def write_global_csv(self):
        # Write global values to CSV
        with open(config.global_csv_file_path, 'w', newline='') as global_csvfile:
            global_fieldnames = ['dsm_file_name', 'epsg_code', 'geopackage_file', 'geopackage_layer',
                                 'starting_point_elevation_from_dsm', 'starting_point_latitude', 'starting_point_longitude']
            global_writer = csv.DictWriter(
                global_csvfile, fieldnames=global_fieldnames)

            global_writer.writeheader()
            global_writer.writerow({
                'dsm_file_name': config.dsm_file_path,
                'epsg_code': self.epsg_code,
                'geopackage_file': config.zone_of_interest_path,
                'starting_point_elevation_from_dsm': self.starting_point_elevation,
                'starting_point_latitude': self.starting_point_transformed[0],
                'starting_point_longitude': self.starting_point_transformed[1]
            })

    def write_waypoint_csv(self):
        # Write waypoints to CSV
        with open(config.points_csv_file_path, 'w', newline='') as points_csvfile:
            points_fieldnames = ['index', 'polygon_id', 'cluster_id',
                                 'distance_from_starting_point', 'latitude', 'longitude', 'elevation_from_dsm']
            points_writer = csv.DictWriter(
                points_csvfile, fieldnames=points_fieldnames)

            points_writer.writeheader()

            for idx, ((lon, lat), elevation, row) in enumerate(zip(self.sorted_points_transformed, self.points_elevation, self.top_polygons_per_cluster.itertuples())):
                points_writer.writerow({
                    'index': idx,
                    'polygon_id': row.Index,  # or row.fid if it's available
                    'cluster_id': row.cluster_id,
                    'distance_from_starting_point': row.distance_to_start,
                    'latitude': lat,
                    'longitude': lon,
                    'elevation_from_dsm': elevation
                })
