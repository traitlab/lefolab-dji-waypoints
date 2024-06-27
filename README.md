# lefolab-drone-src

App and integration with drone

# Prepare package

```bash
python setup.py sdist bdist_wheel
```

# Installation

```bash
mkdir -p /app/lefolab-drone-src
cd /app/lefolab-drone-src
python3 -m venv .venv
source ./.venv/bin/activate
python3 -m pip install --upgrade pip
pip install git+https://vince7lf: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@github.com/vincelf-IVADO/lefolab-drone-src.git
sudo pip show lefolab-drone-src
```

# Requirements

- geopackage of the polygons of the tree crowns
- geoTIFF of the DSM
- geopackage of the polygon of the area of interest
- WGS84 global coordinates of the take off point
- attribute `cluster_id` in the geopackage of the polygons
- attribute `Shape_Area` in the geopackage of the polygons

# Configuration

Configuration file should be located under `/usr/local/etc/lefolab-drone-src/settings.yaml`

Here is a configuration sample : 

```yaml
num_waypoints_per_cluster: 15
flight_height: 400
# <wpml:height>385.799987792969</wpml:height> Voir Google Earth qui est altitude orthométrique
# conversion GPSh NRCAN.GC.CA
point_dsm_height_buffer: 10
# buffer is added to the flight height
# it's also used to add a buffer to the height above the tree for the picture

takeoff_point_wgs84_global_laty_lonx: "45.535075, -73.149231"
takeoff_point_file_path: '/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_starting_point.gpkg'

from_epsg: "epsg:32618"
to_epsg: "epsg:4326"

tree_polygons_file_path: '/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1.gpkg'
zone_of_interest_path: '/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_zone_of_interest.gpkg'
dsm_file_path: '/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_dsm_highdis.cog.tif'

global_csv_file_path: '/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_global_values.csv'
points_csv_file_path: '/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_waypoints.csv'
shortest_path_csv_file_path: '/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_waypoints_shortest_path.csv'

kml_model_file_path: '/usr/local/etc/lefolab-drone-src/wpml/model/Waypoint2/wpmz/template.kml'
output_kml_file_path: '/data/xprize/20240529_sblz1z2_p1/wpmz/template.kml'

wpml_model_file_path: '/usr/local/etc/lefolab-drone-src/wpml/model/Waypoint2/wpmz/waylines.wpml'
output_wpml_file_path: '/data/xprize/20240529_sblz1z2_p1/wpmz/waylines.wpml'

kmz_base_name: '20240529_sblz1z2_p1'
kmz_root_file_path: '/data/xprize'
```

Two other files are needed: 
- ./config/waylines_placemark_no_action.json
- ./config/waylines_placemark_with_actions.json

## Steps to configure: 
```bash
# config
sudo mkdir -p /usr/local/etc/lefolab-drone-src
sudo mkdir -p /usr/local/etc/lefolab-drone-src/wpml/model/Waypoint2/wpmz
cd /usr/local/etc/lefolab-drone-src
sudo vi settings.yaml

# KML and WPML models 
cd /usr/local/etc/lefolab-drone-src/wpml/model/Waypoint2/wpmz
sudo wget https://github.com/vincelf-IVADO/lefolab-drone-src/blob/main/scripts/wpml/model/Waypoint2/wpmz/template.kml
sudo wget https://github.com/vincelf-IVADO/lefolab-drone-src/blob/main/scripts/wpml/model/Waypoint2/wpmz/waylines.wpml

# test data
mkdir -p /data/xprize/20240529_sblz1z2_p1
cd /data/xprize/20240529_sblz1z2_p1
sudo wget https://github.com/vincelf-IVADO/lefolab-drone-src/blob/main/test/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1.gpkg
sudo wget https://github.com/vincelf-IVADO/lefolab-drone-src/blob/main/test/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_zone_of_interest.gpkg
sudo wget https://github.com/vincelf-IVADO/lefolab-drone-src/blob/main/test/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_dsm_highdis.cog.tif
```


# Run

```bash
source ./.venv/bin/activate
PYTHONPATH=$PYTHONPATH:.:./src
python3 -m ./src/main.py
```
