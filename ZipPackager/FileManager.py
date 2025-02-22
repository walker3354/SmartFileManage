from ZipPackager.ZipFileGenerator import ZipGenerator
from concurrent.futures import ThreadPoolExecutor
from Common.JsonLoader import JsonLoader
from threading import Lock
import os, shutil, time

path = JsonLoader("zip_path").load_item()
compressed_file_types = JsonLoader("compressed_file_types").load_item()
image_types = JsonLoader("image_types").load_item()
"""
folder <-folder name            
└── files
└── images
"""


class FileManager:

    def __init__(self):
        self.error_list = dict()
        self.lock = Lock()
        self.zip_generater = ZipGenerator()
        self.folder_list = self.scan_folder()

    def execute(self):
        compress_list = list()
        for folder_name in self.folder_list:
            result = self.check_folder_correctness(folder_name)
            print(result)
            if result == 2:
                compress_list.append(folder_name)
            else:
                continue
        for folder_name in compress_list:
            print(f"compressing {folder_name}")
            self.compress_files(folder_name)

    def scan_folder(self):
        contents = os.listdir(path)
        if contents.count == 0:
            print("the folder is empty")
            return list()
        folder_name_set = list()
        for folder_name in contents:
            if os.path.isdir(os.path.join(path,folder_name)) == True:
                folder_name_set.append(folder_name)
        return folder_name_set

    def extract_extention_name(self, file_name):
        return file_name.split(".")[-1]
    
    def remove_dir_img_in_list(self, original_list):
        image_list = list()
        for content in original_list:
            if self.extract_extention_name(content) in image_types:
                image_list.append(content)
                original_list.remove(content)
        return original_list, image_list

    def check_folder_correctness(self, folder_name):#(0.empty folder (1.already finish (2.unfinish (3.folder error
        folder_path = os.path.join(path, folder_name)
        folder_contents = os.listdir(folder_path)
        if len(folder_contents) == 0:#(0)
            return 0
        content_list, image_list = self.remove_dir_img_in_list(folder_contents)
        if len(image_list) > 0 and len(content_list) == 1 and self.extract_extention_name(content_list[0]) in compressed_file_types:#(1)
            return 1
        if len(image_list) > 0 and len(content_list) > 0:#(2)
            return 2
        else:
            return 3

    def compress_files(self, folder_name):
        folder_path = os.path.join(path, folder_name)
        folder_contents = os.listdir(folder_path)
        content_list, image_list = self.remove_dir_img_in_list(folder_contents)
        self.zip_generater.compress_files(folder_path,content_list)

