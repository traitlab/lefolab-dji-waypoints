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

# Load the zone of interest layer from GeoPackage (if provided)
zone_of_interest_path = 'path_to_geopackage.gpkg'
zone_of_interest_layer = 'zone_of_interest_layer'
try:
    zone_of_interest_gdf = gpd.read_file(
        zone_of_interest_path, layer=zone_of_interest_layer)
    zone_of_interest_provided = True
except ValueError:
    zone_of_interest_provided = False

starting_point = starting_point_gdf.geometry.iloc[0]

# Load the DSM raster data
dsm_path = 'path_to_dsm_layer.tif'
dsm_dataset = rasterio.open(dsm_path)

# Filter trees to only include those within the zone of interest (if provided)
if zone_of_interest_provided and not zone_of_interest_gdf.empty:
    trees_in_zone_gdf = gpd.overlay(
        trees_gdf, zone_of_interest_gdf, how='intersection')
else:
    trees_in_zone_gdf = trees_gdf

# Calculate the centroid for each tree polygon
trees_in_zone_gdf['centroid'] = trees_in_zone_gdf.geometry.centroid

# Group trees by cluster_id
clusters = trees_in_zone_gdf.groupby('cluster_id')

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

# Create KML file compatible with DJI
kml = simplekml.Kml()
document = kml.newdocument(name='DJI Waypoints')

# Add starting point (no elevation adjustment needed)
start = kml.newpoint(name="Start", coords=[
                     (starting_point.x, starting_point.y)])
start.description = "Takeoff Point"
start.altitudemode = simplekml.AltitudeMode.relativetoground
start.altitude = 0

# Add waypoints in sorted order with elevation and additional parameters for DJI
for i, (point, elevation) in enumerate(zip(sorted_points, elevations)):
    wp = kml.newpoint(name=f"Waypoint {i+1}",
                      coords=[(point.x, point.y, elevation)])
    wp.altitudemode = simplekml.AltitudeMode.relativetoground
    wp.altitude = elevation
    wp.extrude = 1
    wp.lookat = simplekml.LookAt(
        longitude=point.x,
        latitude=point.y,
        altitude=elevation,
        heading=0,
        tilt=90,
        range=10,
        altitudemode=simplekml.AltitudeMode.relativetoground
    )
    wp.description = "Take photo here"
    # Add any additional DJI-specific parameters if needed

# Save KML file
kml.save('dji_waypoints_with_elevation.kml')
