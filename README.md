# lefolab-drone-src

App and integration with drone

# Prepare package

```
python setup.py sdist bdist_wheel
```

# Installation

```
python3 -m venv .venv
source ./.venv/bin/activate
python3 -m pip install --upgrade pip
pip install git+https://vince7lf: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@github.com/vincelf-IVADO/lefolab-drone-src.git
```

# Configuration

Configuration file should be located under `/usr/local/etc/lefolab_drone_src/settings.yaml`

Here is a configuration sample : 

```yaml
num_waypoints_per_cluster: 5

tree_polygons_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1.gpkg'
starting_point_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_starting_point.gpkg'
zone_of_interest_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_zone_of_interest.gpkg'
dsm_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_dsm_highdis.cog.tif'

global_csv_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_global_values.csv'
points_csv_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_waypoints.csv'

kml_model_file_path: './scripts/wpml/model/Waypoint2/wpmz/template.kml'
output_kml_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/wpmz/template.kml'

wpml_model_file_path: 'scripts/wpml/model/Waypoint2/wpmz/waylines.wpml'
output_wpml_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/wpmz/waylines.wpml'

kmz_base_name: '20240529_sblz1z2_p1'
kmz_root_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize'
```