import csv

import geopandas as gpd
import numpy as np
import rasterio
from pyproj import Transformer

from lib.config import config
from lib.takeoff_point import TakeOffPoint


class ExtractPoints:
    def __init__(self):
        self.zone_of_interest_gdf = None
        self.takeoff_point_gdf = None
        self.trees_gdf = None
        self.trees_in_zone_gdf = None
        self.clusters = None
        self.top_polygons_per_cluster = None
        self.epsg_code = None
        self.random_points = []
        self.sorted_points = None
        self.points_elevation = None
        self.takeoff_point_elevation = None
        self.sorted_points_transformed = None
        self.takeoff_point_transformed = None
        self.highest_elevation = 0

    # Function to read zone of interest GeoDataFrame
    def read_zone_of_interest_gdf(self):
        try:
            self.zone_of_interest_gdf = gpd.read_file(
                config.zone_of_interest_path)
        except ValueError as e:
            # Log error
            print(f"Error reading GeoDataFrame: {e}")

    def load(self):

        takeoff_point = TakeOffPoint()
        takeoff_point.setup()
        takeoff_point.reproject()
        takeoff_point.save()

        # Load the starting point and clusters layers from GeoPackage
        self.takeoff_point_gdf = gpd.read_file(
            config.takeoff_point_file_path)
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

    def get_highest_point_from_DSM(self):
        self.highest_elevation = np.max(
            self.dsm_dataset.read(1))  # Read the first band

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

        # Select the top polygons with the greatest area among the closest ones
        top_polygons = sorted_polygons.nlargest(
            config.num_waypoints_per_cluster, 'Shape_Area')

        return top_polygons

    def setup(self):
        self.takeoff_point = self.takeoff_point_gdf.geometry.iloc[0]

        # Calculate the centroid for each tree polygon
        self.trees_in_zone_gdf['centroid'] = self.trees_in_zone_gdf.geometry.centroid
        # self.trees_in_zone_gdf['area'] = self.trees_in_zone_gdf.area
        self.trees_in_zone_gdf['distance_to_start'] = self.trees_in_zone_gdf['centroid'].distance(
            self.takeoff_point)
        self.trees_in_zone_gdf['polygon_id'] = self.trees_in_zone_gdf.index

        # Group trees by cluster_id
        self.clusters = self.trees_in_zone_gdf.groupby('cluster_id')

        # Apply the function to each group
        self.top_polygons_per_cluster = self.clusters.apply(
            self.select_top_polygons)

        # Reset index
        self.top_polygons_per_cluster.reset_index(drop=True, inplace=True)

        # # Sort each group by area attribute and select top polygons
        # self.top_polygons_per_cluster = self.clusters.apply(
        #     lambda x: x.nlargest(5, 'area')).reset_index(drop=True)

        # Extract EPSG code
        self.epsg_code = self.trees_in_zone_gdf.crs.to_epsg()

        self.get_highest_point_from_DSM()

    def get_points_elevation_from_dsm(self):
        self.points_elevation = []
        # Iterate over each cluster
        for _, cluster_polygons in self.top_polygons_per_cluster.groupby('cluster_id'):
            # Extract elevations for polygons in the cluster
            cluster_elevations = [self.get_elevation_from_dsm(
                point, self.dsm_dataset) for point in cluster_polygons['centroid']]
            self.points_elevation.extend(cluster_elevations)

        # Calculate elevation of the starting point once
        self.takeoff_point_elevation = self.get_elevation_from_dsm(
            self.takeoff_point, self.dsm_dataset)

    def reproject(self, epsg_from, epsg_to):
        # Transform coordinates
        transformer = Transformer.from_crs(epsg_from, epsg_to)
        self.sorted_points_transformed = [transformer.transform(
            point.x, point.y) for point in self.top_polygons_per_cluster['centroid']]
        self.takeoff_point_transformed = transformer.transform(
            self.takeoff_point.x, self.takeoff_point.y)

    def write_global_csv(self):
        # Write global values to CSV
        with open(config.global_csv_file_path, 'w', newline='') as global_csvfile:
            global_fieldnames = ['dsm_file_name', 'epsg_code', 'geopackage_file',
                                 'takeoff_point_elevation_from_dsm', 'takeoff_point_lon_x', 'takeoff_point_lat_y', 'highest_elevation_from_dsm']
            global_writer = csv.DictWriter(
                global_csvfile, fieldnames=global_fieldnames)

            global_writer.writeheader()
            global_writer.writerow({
                'dsm_file_name': config.dsm_file_path,
                'epsg_code': self.epsg_code,
                'geopackage_file': config.zone_of_interest_path,
                'takeoff_point_elevation_from_dsm': self.takeoff_point_elevation,
                'takeoff_point_lon_x': self.takeoff_point_transformed[1],
                'takeoff_point_lat_y': self.takeoff_point_transformed[0],
                'highest_elevation_from_dsm': self.highest_elevation
            })

    def write_waypoint_csv(self):
        # Write waypoints to CSV
        with open(config.points_csv_file_path, 'w', newline='') as points_csvfile:
            points_fieldnames = ['index', 'polygon_id', 'cluster_id',
                                 'distance_from_takeoff_point', 'lon_x', 'lat_y', 'elevation_from_dsm']
            points_writer = csv.DictWriter(
                points_csvfile, fieldnames=points_fieldnames)

            points_writer.writeheader()

            for idx, ((lat, lon), elevation, row) in enumerate(zip(self.sorted_points_transformed, self.points_elevation, self.top_polygons_per_cluster.itertuples())):
                points_writer.writerow({
                    'index': idx,
                    'polygon_id': row.polygon_id,
                    'cluster_id': row.cluster_id,
                    'distance_from_takeoff_point': row.distance_to_start,
                    'lon_x': lon,
                    'lat_y': lat,
                    'elevation_from_dsm': elevation
                })
