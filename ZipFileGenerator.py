import shutil
import os
import sys


class ZipGenerator:
    def __init__(self, folder_path, sub_folder_title):
        self.full_path = os.path.join(folder_path, sub_folder_title)
        self.folder_path = folder_path
        self.sub_folder_title = sub_folder_title
        self.compress_folder()

    def compress_folder(self):
        if os.path.exists(self.folder_path) and os.path.isdir(self.full_path):
            sys.stdout.write(f"\r{self.sub_folder_title} compressing....")
            sys.stdout.flush()
            output_path = os.path.join(self.folder_path, "game_zip")
            shutil.make_archive(
                output_path, "zip", self.folder_path, self.sub_folder_title
            )
            sys.stdout.write(
                "\r" + " " * len(f"{self.sub_folder_title} compressing....") + "\r"
            )
            sys.stdout.flush()


"""
folder <-folder path            
└── folder<- sub_folder title and full path
"""
