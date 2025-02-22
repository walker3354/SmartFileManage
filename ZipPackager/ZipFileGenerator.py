import zipfile
import os

class ZipGenerator:
    def __init__(self):
        pass

    def compress_files(self, folder_path, content_list):
        zip_file_path = os.path.join(folder_path, "Game1.zip")
        with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for content in content_list:
                full_path = os.path.join(folder_path, content)
                if os.path.isdir(full_path):
                  for root, dirs, files in os.walk(full_path):
                        for f in files:
                            file_path = os.path.join(root, f)
                            arcname = os.path.relpath(file_path, folder_path)
                            zipf.write(file_path, arcname=arcname)
                else:
                    arcname = os.path.basename(full_path)
                    zipf.write(full_path, arcname=arcname)
