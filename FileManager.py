from ZipFileGenerator import ZipGenerator
import os
import shutil
import time

path = "D:\\ZipManager"
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
]


class FileManager:
    def __init__(self):
        self.folder_list = list()
        self.error_list = list()
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

    def compress_file(self):
        for folder_name in self.folder_list:
            result, sub_folder_name = self.check_file_correctness(folder_name)
            if result == True:
                folder_path = os.path.join(path, folder_name)
                ZipGenerator(folder_path, sub_folder_name)
                self.delete_sub_folder(folder_path, sub_folder_name, folder_name)
            else:
                self.error_list.append(folder_name)
        if len(self.error_list) != 0:
            print(f"\n\nsome folder error {self.error_list}")

    def check_file_correctness(self, folder_name):
        filename_extention = str()
        check_extention_result = False
        print("checking file correctness")
        check_extention_result, filename_extention = self.check_filename_extention(
            folder_name
        )
        if self.check_file_num(folder_name) and check_extention_result:
            return True, filename_extention
        else:
            return False, filename_extention

    def check_filename_extention(self, folder_name):
        sub_folder_name = str()
        check_dir_flag = False
        check_img_flag = False
        full_path = os.path.join(path, folder_name)
        file_name_list = os.listdir(full_path)
        print(f"checking folder:{folder_name} file name extention", end=" : ")
        for i in file_name_list:
            if os.path.isdir(full_path + "\\" + i) == True:
                check_dir_flag = True
                sub_folder_name = i
            if (
                os.path.isfile(full_path + "\\" + i) == True
                and image_types.count(i.split(".")[1].lower()) != 0
            ):
                check_img_flag = True
        if check_dir_flag == True and check_img_flag == True:
            print("pass")
            return True, sub_folder_name
        print("error")
        return False, sub_folder_name

    def check_file_num(self, folder_name):
        file_num = os.listdir(path + "\\" + folder_name)
        print(f"checking folder {folder_name} file number", end=" : ")
        if len(file_num) == 2:
            print("pass")
            return True
        print("error")
        return False

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
        self.error_list.append(folder_name)


if __name__ == "__main__":
    file_manager = FileManager()
    file_manager.compress_file()

"""
folder <-folder name            
└── folder<- sub_folder title and full path
"""
