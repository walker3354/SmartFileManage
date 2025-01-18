from ZipFileGenerator import ZipGenerator
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import os
import shutil
import time

path = "D:\\ZipManager"
compressed_file_types = ["zip", "7z", "rar"]
image_types = [
    "jpg",
    "jpeg",
    "png",
    "gif",
    "bmp",
    "tiff",
    "psd",
    "pdf",
    "eps",
    "ai",
    "indd",
    "raw",
    "svg",
    "webp",
    "jfif",
]


class FileManager:
    def __init__(self):
        self.folder_list = list()
        self.error_list = dict()
        self.lock = Lock()
        self.scan_folder()

    def scan_folder(self):
        content = os.listdir(path)
        if content.count == 0:
            print("the folder is empty")
        else:
            self.folder_list = content

    def print_current_folder(self):
        print(f"the total count of folder is {len(self.folder_list)}\n")
        for i in self.folder_list:
            print(f"{i}\n")

    def compress_file(self, folder_name):
        result, sub_folder_name = self.check_folder_correctness(folder_name)
        if result == True and sub_folder_name != "":
            folder_path = os.path.join(path, folder_name)
            ZipGenerator(folder_path, sub_folder_name)
            self.delete_sub_folder(folder_path, sub_folder_name, folder_name)
        elif result == False and sub_folder_name == "compressed":
            print(f"{folder_name} already finished")
        else:
            with self.lock:
                self.error_list[folder_name] = "file content error"

    def multi_compress_file(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            for folder_name in self.folder_list:
                executor.submit(self.compress_file, folder_name)
        if len(self.error_list.keys()) != 0:
            print(f"\n\nsome folder error {self.error_list}")

    def check_folder_correctness(self, folder_name):
        other_file_counter = 0
        compress_flag = False
        image_flag = False
        sub_folder_name = str()
        error_file_list = list()
        for file_name in os.listdir(os.path.join(path, folder_name)):
            full_path = os.path.join(os.path.join(path, folder_name), file_name)
            if (
                os.path.isdir(full_path) == False
                and file_name.split(".")[1] in image_types
            ):
                image_flag = True
            elif (
                os.path.isdir(full_path) == False
                and file_name.split(".")[1] in compressed_file_types
            ):
                compress_flag = True
                other_file_counter += 1
                error_file_list.append(file_name)
            else:
                other_file_counter += 1
                error_file_list.append(file_name)
                sub_folder_name = file_name
        if image_flag == True and compress_flag == False and other_file_counter == 1:
            return True, sub_folder_name
        elif image_flag == True and other_file_counter > 1:
            sub_folder_name = self.organize_unrelated_data(folder_name, error_file_list)
            return True, sub_folder_name
        elif compress_flag == True and image_flag == True and other_file_counter == 1:
            return False, "compressed"
        else:
            return False, ""

    def organize_unrelated_data(self, folder_name, file_list):
        folder_path = os.path.join(path, folder_name)
        sub_folder_path = os.path.join(folder_path, "new_game_folder")
        if os.path.exists(sub_folder_path):
            pass
        else:
            os.makedirs(sub_folder_path)
        for file in file_list:
            if file == "new_game_folder":
                continue
            shutil.move(os.path.join(folder_path, file), sub_folder_path)
        return sub_folder_path

    def delete_sub_folder(self, folder_path, sub_folder_name, folder_name):
        retries = 3
        print(f"deleting {sub_folder_name}")
        for i in range(retries):
            try:
                full_path = os.path.join(folder_path, sub_folder_name)
                shutil.rmtree(full_path)
                return
            except PermissionError as e:
                time.sleep(3)
        with self.lock:
            self.error_list[folder_name] = "delete error"


if __name__ == "__main__":
    file_manager = FileManager()
    file_manager.multi_compress_file()

"""
folder <-folder name            
└── folder<- sub_folder title and full path
"""
