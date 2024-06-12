import random

import geopandas as gpd
import numpy as np
import rasterio
import simplekml
from shapely.geometry import Point

# Load the starting point and clusters layers from GeoPackage
starting_point_gdf = gpd.read_file(
    'path_to_geopackage.gpkg', layer='starting_point_layer')
trees_gdf = gpd.read_file('path_to_geopackage.gpkg', layer='trees_layer')

starting_point = starting_point_gdf.geometry.iloc[0]

# Load the DSM raster data
dsm_path = 'path_to_dsm_layer.tif'
dsm_dataset = rasterio.open(dsm_path)

# Calculate the centroid for each tree polygon
trees_gdf['centroid'] = trees_gdf.geometry.centroid

# Group trees by cluster_id
clusters = trees_gdf.groupby('cluster_id')

# Select random centroids for each cluster
num_waypoints_per_cluster = 5
random_points = []

for cluster_id, cluster in clusters:
    if len(cluster) <= num_waypoints_per_cluster:
        selected_trees = cluster
    else:
        selected_trees = cluster.sample(num_waypoints_per_cluster)
    random_points.extend(selected_trees['centroid'].tolist())

# Function to calculate distance between two points


def calculate_distance(point1, point2):
    return point1.distance(point2)


# Create a list of tuples (point, distance)
points_with_distances = [(point, calculate_distance(
    starting_point, point)) for point in random_points]
# Sort points by distance
points_with_distances.sort(key=lambda x: x[1])

# Extract sorted points
sorted_points = [point for point, _ in points_with_distances]

# Function to extract elevation from DSM for a given point


def get_elevation_from_dsm(point, dataset):
    coords = [(point.x, point.y)]
    for val in dataset.sample(coords):
        return val[0]


# Extract elevation for each point and adjust for tree height (10 meters above DSM elevation)
elevations = [get_elevation_from_dsm(
    point, dsm_dataset) + 10 for point in sorted_points]

# Create KML file
kml = simplekml.Kml()
# Add starting point (no elevation adjustment needed)
kml.newpoint(name="Start", coords=[(starting_point.x, starting_point.y)])

# Add waypoints in sorted order with elevation
for i, (point, elevation) in enumerate(zip(sorted_points, elevations)):
    kml.newpoint(name=f"Waypoint {i+1}",
                 coords=[(point.x, point.y, elevation)])

# Save KML file
kml.save('waypoints_with_elevation.kml')
