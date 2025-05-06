# lefolab-dji-waypoints
## Setup

```bash
# Clone the module into /opt/treesight 
cd /opt/treesight
git clone https://github.com/traitlab/lefolab-dji-waypoints.git
cd lefolab-dji-waypoints

# Checkout v2
git checkout v2

# create conda venv
source /opt/miniconda3/bin/activate
conda create --yes --name dji-waypoints python=3.8
conda activate dji-waypoints

# Update pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create output test folder
mkdir -p test/output
```

## Generate the waypoints
### Admin user

```bash
source /opt/miniconda3/bin/activate
conda activate dji-waypoints
# mandatory because kml and wpml models are relative
cd /opt/treesight/lefolab-dji-waypoints
python src/main.py --csv ./test/input/test_one_wpt.csv --output ./test/output
```

### User

```bash
source /opt/miniconda3/bin/activate
conda activate dji-waypoints
# mandatory because kml and wpml models are relative
cd /opt/treesight/lefolab-dji-waypoints
python /opt/treesight/lefolab-dji-waypoints/src/main.py --csv /data/<username>/input/test_one_wpt.csv --output /data/<username>/output
```

## Validate

Using the command and input CSV aboce, the generated files are : 

```bash
test/ouput/
└── test-one-wpt
    ├── test-one-wpt.kmz
    └── wpmz
        ├── template.kml
        └── waylines.wpml
```

```bash
test/ouput/test-one-wpt/:
total 16
drwxrwsr-x 3 lefolab treesight 4096 May  6 11:00 ..
drwxrwsr-x 2 lefolab treesight 4096 May  6 11:00 wpmz
drwxrwsr-x 3 lefolab treesight 4096 May  6 11:00 .
-rw-rw-r-- 1 lefolab treesight 3463 May  6 11:17 test-one-wpt.kmz

test/ouput/test-one-wpt/wpmz:
total 36
drwxrwsr-x 3 lefolab treesight  4096 May  6 11:00 ..
drwxrwsr-x 2 lefolab treesight  4096 May  6 11:00 .
-rw-rw-r-- 1 lefolab treesight 12089 May  6 11:17 template.kml
-rw-rw-r-- 1 lefolab treesight 13785 May  6 11:17 waylines.wpml
```

## Debug mode

Using option `--debug (-d)` will add the datetime to the kmz file (`20240529_sblz1z2_p1_20250428T161738.kmz`)

