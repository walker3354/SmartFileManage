import json

path = "spec.json"


class JsonLoader:

    def __init__(self, item):
        self.item = item

    def load_item(self):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data[self.item]


def load_pic_path():
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["pic_path"]


def load_pic_standard():
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["pic_standard"]


def load_zip_path():
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["zip_path"]


def load_compressed_file_types():
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["compressed_file_types"]


def load_image_types():
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["image_types"]
