import os
import zipfile
from datetime import datetime

from lib.config import config


class CreateKMZ:
    def __init__(self):
        # File paths
        # Get current datetime
        current_datetime = datetime.now().strftime("%Y%m%dT%H%M%S")
        self.wpmz_dir = f"{config.kmz_root_file_path}/{config.kmz_base_name}/wpmz"
        self.kmz_file_path = f"{config.kmz_root_file_path}//{config.kmz_base_name}/{config.kmz_base_name}_{current_datetime}.kmz"

    def create_kmz(self):

        # Create the KMZ file
        with zipfile.ZipFile(self.kmz_file_path, 'w', zipfile.ZIP_DEFLATED) as kmz:
            for folder_name, _, filenames in os.walk(self.wpmz_dir):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    arcname = os.path.relpath(file_path, self.wpmz_dir)
                    kmz.write(file_path, arcname)
