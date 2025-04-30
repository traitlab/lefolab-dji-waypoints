import os
import zipfile
from datetime import datetime


def create_kmz(base_dir, kmz_filename):

    # Create the KMZ file
    with zipfile.ZipFile(kmz_filename, 'w', zipfile.ZIP_DEFLATED) as kmz:
        for folder_name, _, filenames in os.walk(base_dir):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                arcname = os.path.relpath(file_path, base_dir)
                kmz.write(file_path, arcname)


# File paths
# Get current datetime
current_datetime = datetime.now().strftime("%Y%m%dT%H%M%S")
basename = f'20240529_sblz1z2_p1'
base_dir = f"/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/{basename}/wpmz"
kmz_file = f"/mnt/c/Users/vincent.le.falher/Downloads/UdeM/xprize/{basename}/{basename}_{current_datetime}.kmz"

# Create the KMZ file
create_kmz(base_dir, kmz_file)
