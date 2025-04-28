# lefolab-dji-waypoints

App and integration with drone

# Installation

```bash
cd /app
git clone https://vince7lf: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@github.com/vincelf-IVADO/lefolab-dji-waypoints.git
cd /app/lefolab-dji-waypoints
python3 -m venv .venv
source ./.venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

# Requirements

- CSV file containing the points to be used to generate the waypoint mission.

# Configuration

Configuration file should be located under `/app/lefolab-dji-waypoints/config`. 

Samples are given (`settings.yaml`, `settings@lefotitan_20240529_sblz1z2_p1.yaml`)

Here is a configuration sample : 

```yaml
flight_height: 400
takeoff_point_elevation: 331
# <wpml:height>385.799987792969</wpml:height> Voir Google Earth qui est altitude orthométrique
# conversion GPSh NRCAN.GC.CA
point_dsm_height_approach: 5
point_dsm_height_buffer: 10
# buffer is added to the flight height
# it's also used to add a buffer to the height above the tree for the picture

base_path: '/data/xprize'
base_name: '20240529_sblz1z2_p1'
points_csv_file_path: '/data/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_waypoints_shortest_path.csv'

# required depending on the installation path. If started from the project folder, no need as defaujlt is relative to project folder.
# kml_model_file_path: '/opt/treesight/lefolab-dji-waypoints/scripts/wpml/model/Waypoint2/wpmz/template.kml'
# wpml_model_file_path: '/opt/treesight/lefolab-dji-waypoints/scripts/wpml/model/Waypoint2/wpmz/waylines.wpml'
# waylines_placemark_no_action: '/opt/treesight/lefolab-dji-waypoints/config/waylines_placemark_no_action.json'
# waylines_placemark_with_actions: '/opt/treesight/lefolab-dji-waypoints/config/waylines_placemark_with_action.json'
```

# test data
```
mkdir -p /data/xprize/20240529_sblz1z2_p1
cd /data/xprize/20240529_sblz1z2_p1
# Downdload data from Google Drive using browser
# https://drive.google.com/drive/folders/1A_qd60c40s3TuK89o3ZAFM27lRA-5KbS?usp=drive_link
# copy from Downloads to /data/xprize/20240529_sblz1z2_p1
cp ~/Downloads/20240529_sblz1z2_p1.gpkg /data/xprize/20240529_sblz1z2_p1
cp ~/Downloads/20240529_sblz1z2_p1_zone_of_interest.gpkg /data/xprize/20240529_sblz1z2_p1
cp ~/Downloads/20240529_sblz1z2_p1_dsm_highdis.cog.tif /data/xprize/20240529_sblz1z2_p1
```

# Run

```bash
cd /app/lefolab-dji-waypoints
source /app/lefolab-dji-waypoints/.venv/bin/activate
python /app/lefolab-dji-waypoints/src/main.py --config /app/lefolab-dji-waypoints/config/settings@lefotitan_20240529_sblz1z2_p1.yaml
```
# Results 

Generated files (KMZ, wpmz/template.kml, wpmz/waylines.wpml) are located in :
`/app/lefolab-dji-waypoints/output/`


# Command line : 

--flight_height -ft 400 --takeoff_point_elevation -tpe 331 --point_dsm_height_approach -pdha 5 --point_dsm_height_buffer -pdhb 10 --ouput '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize' --csv '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_waypoints_shortest_path.csv' 

mission = csv basename (20240529_sblz1z2_p1)
output path : /mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize
output name : 20240529_sblz1z2_p1.kmz (overwrite)

```bash
flight_height: 400
takeoff_point_elevation: 331
# <wpml:height>385.799987792969</wpml:height> Voir Google Earth qui est altitude orthométrique
# conversion GPSh NRCAN.GC.CA
point_dsm_height_approach: 5
point_dsm_height_buffer: 10
# buffer is added to the flight height
# it's also used to add a buffer to the height above the tree for the picture

base_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize'
base_name: '20240529_sblz1z2_p1'
points_csv_file_path: '/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/20240529_sblz1z2_p1/20240529_sblz1z2_p1_waypoints_shortest_path.csv'
```
