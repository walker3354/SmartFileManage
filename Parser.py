from ZipPackager.FileManager import FileManager
from ImgComparer.ImageReader import ImageReader


class Parser:

    def __init__(self):
        self.action_dict = {"zip": self.executet_filemanager,"image": self.execute_imagereader}
        self.menu_map = {'1': 'zip','2': 'image'}

    def execute(self):
        while True:
            self.print_function_menu()
            command = input("please select commnad: ")
            if command == '0':
                break
            if command in self.menu_map:
                key_for_action = self.menu_map[command]
                self.action_dict[key_for_action]()
            else:
                print("unknown command !!")

    def execute_imagereader(self):
        img_reader = ImageReader()
        img_reader.execute()
        if len(img_reader.similarity_list) != 0:
            print("\nfind similarit!!!\n")
            for i in img_reader.similarity_list:
                print(i)
        else:
            print("pass")

    def executet_filemanager(self):
        print("processing............")
        FileManager().execute()
        print("finished whole process")

    def print_function_menu(self):
        print("\t0)Exit")
        print("\t1)Zip files generate")
        print("\t2)Image files detect")
