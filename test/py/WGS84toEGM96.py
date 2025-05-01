## Download the EGM96 geoid model file using curl
import pyproj
import requests
import os

# Get the pyproj data directory
proj_download_dir = pyproj.datadir.get_data_dir()

# Create the directory if it doesn't exist
if not os.path.exists(proj_download_dir):
    os.makedirs(proj_download_dir)

# Define the URL of the file to download
url = "https://cdn.proj.org/us_nga_egm96_15.tif"

# Define the path to save the file
file_path = os.path.join(proj_download_dir, "us_nga_egm96_15.tif")

# Check if the file already exists
if not os.path.exists(file_path):
    # Download the file
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

from pyproj.crs import CompoundCRS
cmpd_crs = CompoundCRS(name="WGS 84 + EGM96 height", components=["EPSG:4326", "EPSG:5773"])
print(cmpd_crs)

lon = -74.0054965099865
lat = 45.9894202250383
ellips_height = 366.566619873047

trans = pyproj.Transformer.from_crs("EPSG:4979", cmpd_crs, always_xy=True)
lon_out, lat_out, egm96_height = trans.transform(lon, lat, ellips_height)

print(egm96_height)


