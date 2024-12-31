import shutil
import os

"""
folder <-folder path            
└── folder<- sub_folder title and full path
"""


class ZipGenerator:
    def __init__(self, folder_path, folder_title):
        self.full_path = os.path.join(folder_path, folder_title)
        self.folder_path = folder_path
        self.folder_title = folder_title
        self.compress_folder()

    def compress_folder(self):
        if os.path.exists(self.folder_path) and os.path.isdir(self.full_path):
            output_path = os.path.join(self.folder_path, "game_zip")
            shutil.make_archive(output_path, "zip", self.folder_path, self.folder_title)
