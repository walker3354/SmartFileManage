from ZipPackager.ZipFileGenerator import ZipGenerator
from concurrent.futures import ThreadPoolExecutor
from Common.JsonLoader import JsonLoader
from threading import Lock
import os, shutil

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

    def scan_folder(self):
        contents = os.listdir(path)
        if contents.count == 0:
            print("the folder is empty")
            return list()
        folder_name_set = list()
        for content_name in contents:
            if os.path.isdir(os.path.join(path,content_name)) == True:
                folder_name_set.append(content_name)
        return folder_name_set

    def execute(self):
        compress_list = list()
        for folder_name in self.folder_list:
            result = self.check_folder_correctness(folder_name)
            if result == 2:
                compress_list.append(folder_name)
            else:
                continue
        self.multi_compress_files(compress_list)

    def extract_extention_name(self, file_name):
        return file_name.split(".")[-1]
    
    def remove_dir_img_in_list(self, original_list):
        image_list = list()
        for content in original_list.copy():
            if self.extract_extention_name(content) in image_types:
                image_list.append(content)
                original_list.remove(content)
        return original_list, image_list

    def check_folder_correctness(self, folder_name):#(0.empty folder (1.already finished (2.unfinish (3.folder error
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
            print(f"\t folder error, path: {folder_path}")
            return 3

    def compress_files(self, folder_name):
        folder_path = os.path.join(path, folder_name)
        folder_contents = os.listdir(folder_path)
        content_list, image_list = self.remove_dir_img_in_list(folder_contents)
        self.zip_generater.compress_files(folder_path,content_list)
        self.delete_compressed_files(folder_name,content_list)

    
    def delete_compressed_files(self,folder_name,content_list):
        folder_path  = os.path.join(path,folder_name)
        for conetent_name in content_list:
            conetent_path = os.path.join(folder_path,conetent_name)
            if os.path.isdir(conetent_path) == True:
                shutil.rmtree(conetent_path)
            else:
                os.remove(conetent_path)


    def multi_compress_files(self,folder_name_set):
        max_workers = 5
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.compress_files, folder_name) for folder_name in folder_name_set]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"Error compressing folder: {e}")
