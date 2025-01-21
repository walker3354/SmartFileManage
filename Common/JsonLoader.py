import json

path = "spec.json"


class JsonLoader:

    def __init__(self, item):
        self.item = item

    def load_item(self):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data[self.item]
