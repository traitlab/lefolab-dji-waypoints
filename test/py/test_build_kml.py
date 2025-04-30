import csv

import geopandas as gpd
import rasterio

# Load the starting point and clusters layers from GeoPackage
starting_point_gdf = gpd.read_file(
    '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240521_zf2100ha_lowres_m3m/starting_point.gpkg', layer='starting_point')
trees_gdf = gpd.read_file('/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240521_zf2100ha_lowres_m3m/20240521_zf2100ha_highres_m3m_rgb_gr0p05_inferclassifier_fixed_subset.gpkg',
                          layer='20240521_zf2100ha_highres_m3m_rgb_gr0p05_inferclassifier_fixed_subset')

# Load the zone of interest layer from GeoPackage (if provided)
zone_of_interest_path = '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240521_zf2100ha_lowres_m3m/zf2100ha_clusters_of_interest.gpkg'
zone_of_interest_layer = 'zone_of_insterest'
try:
    zone_of_interest_gdf = gpd.read_file(
        zone_of_interest_path, layer=zone_of_interest_layer)
    zone_of_interest_provided = True
except ValueError:
    zone_of_interest_provided = False

starting_point = starting_point_gdf.geometry.iloc[0]

# Load the DSM raster data
dsm_path = '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240521_zf2100ha_lowres_m3m/20240521_zf2100ha_lowres_m3m_dsm_subset.tif'
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


# CSV file path
csv_file_path = 'waypoints.csv'

# Extract EPSG code
epsg_code = trees_in_zone_gdf.crs.to_epsg()

# Calculate elevation of the starting point once
starting_point_elevation = get_elevation_from_dsm(starting_point, dsm_dataset)


# CSV file paths
global_csv_file_path = 'global_values.csv'
points_csv_file_path = 'waypoints.csv'

# Calculate elevation of the starting point once
starting_point_elevation = get_elevation_from_dsm(starting_point, dsm_dataset)

# Write global values to CSV
with open(global_csv_file_path, 'w', newline='') as global_csvfile:
    global_fieldnames = ['dsm_file_name', 'epsg_code', 'geopackage_file', 'geopackage_layer',
                         'starting_point_elevation_from_dsm', 'starting_point_latitude', 'starting_point_longitude']
    global_writer = csv.DictWriter(
        global_csvfile, fieldnames=global_fieldnames)

    global_writer.writeheader()
    global_writer.writerow({
        'dsm_file_name': dsm_path,
        'epsg_code': epsg_code,
        'geopackage_file': zone_of_interest_path,
        'geopackage_layer': zone_of_interest_layer,
        'starting_point_elevation_from_dsm': starting_point_elevation,
        'starting_point_latitude': starting_point.y,
        'starting_point_longitude': starting_point.x
    })

# Write waypoints to CSV
with open(points_csv_file_path, 'w', newline='') as points_csvfile:
    points_fieldnames = ['index', 'polygon_id', 'cluster_id',
                         'distance_from_starting_point', 'latitude', 'longitude', 'elevation_from_dsm']
    points_writer = csv.DictWriter(
        points_csvfile, fieldnames=points_fieldnames)

    points_writer.writeheader()

    for idx, (point, elevation) in enumerate(zip(sorted_points, elevations)):
        points_writer.writerow({
            'index': idx,
            'polygon_id': 0,
            'cluster_id': 0,
            'distance_from_starting_point': points_with_distances[idx][1],
            'latitude': point.y,
            'longitude': point.x,
            'elevation_from_dsm': elevation
        })
