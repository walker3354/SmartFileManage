import os

path = "D:\\test_folder"


class ImageReader:
    def __init__(self):
        self.sub_folder_list = []

    def scan_folder(self):
        self.sub_folder_list = os.listdir(path)
        if len(self.sub_folder_list) == 0:
            return False
        return True
    
    def 


"""
main_folder
└──sub_folder = {pic1,pic2......}
└──sub_folder = {pic1,pic2......}
"""
