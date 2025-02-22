from torchvision import models, transforms
from PIL import Image
from Common.JsonLoader import JsonLoader
import torch
import os
import json

standard = JsonLoader("pic_standard").load_item()
path = JsonLoader("pic_path").load_item()
log_path = os.path.join(path, "json_logs")
image_types = JsonLoader("image_types").load_item()


class ImageReader:

    def __init__(self):
        self.sub_folder_list = []
        self.log_folder_name = []
        self.feature = dict()
        self.similarity_list = []
        self.relevance_list = []
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(
            weights=models.ResNet50_Weights.DEFAULT).to(self.device)
        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
        self.model.eval()
        self.scan_logs()
        self.scan_folder()

    def scan_logs(self):
        if os.path.isdir(log_path):
            self.log_folder_name = [
                os.path.splitext(file)[0]  # 去掉 .json 後綴
                for file in os.listdir(log_path)
                if os.path.isfile(os.path.join(log_path, file))
            ]
        self.sub_folder_list.extend(self.log_folder_name)

    def scan_folder(self):
        folder_list = [
            folder for folder in os.listdir(path)
            if os.path.isdir(os.path.join(path, folder))
        ]
        self.sub_folder_list = list(set(self.sub_folder_list + folder_list))
        if len(self.sub_folder_list) == 0:
            return False
        if "json_logs" in self.sub_folder_list:
            self.sub_folder_list.remove("json_logs")
        return True

    def scan_sub_folder_pic(self, sub_folder_name):
        full_path = os.path.join(path, sub_folder_name)
        sub_folder_images_path = []
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            if os.path.isfile(file_path) and file.split(
                    ".")[-1].lower() in image_types:
                sub_folder_images_path.append(file_path)
        return sub_folder_images_path

    def check_log(self, sub_folder):
        if os.path.isfile(os.path.join(log_path, f"{sub_folder}.json")):
            if sub_folder not in self.sub_folder_list:
                self.sub_folder_list.append(sub_folder)
            return True
        return False

    def create_log(self, sub_folder, features):
        data = {}
        for i, feature in enumerate(features):
            data[f"feature_{i}"] = feature.cpu().numpy().tolist()
        os.makedirs(log_path, exist_ok=True)
        file_path = os.path.join(log_path, f"{sub_folder}.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def read_log(self, sub_folder):  # folder/json_logs/save.json
        file_path = os.path.join(log_path, f"{sub_folder}.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        features = []
        for key in sorted(data.keys()):
            features.append(torch.tensor(data[key]))
        return torch.stack(features).to(self.device)

    def extract_features(self, sub_folder, image_paths):
        images = []
        if self.check_log(sub_folder) == True:
            return self.read_log(sub_folder)
        for image_path in image_paths:
            images.append(
                self.preprocess(Image.open(image_path).convert("RGB")))
        images = torch.stack(images).to(self.device)
        with torch.no_grad():
            features = self.model(images)
        self.create_log(sub_folder, features)
        return features

    def execute(self):
        for sub_folder in self.sub_folder_list:
            print(f'extracting "{sub_folder}" content')
            if self.check_log(sub_folder):  # 如果 log 存在，直接讀取
                self.feature[sub_folder] = self.read_log(sub_folder)
            else:
                image_paths = self.scan_sub_folder_pic(sub_folder)
                self.feature[sub_folder] = self.extract_features(
                    sub_folder, image_paths)
        feature_keys = list(self.feature.keys())
        for i in range(len(self.feature.values()) - 1):
            for j in range(i + 1, len(self.feature.values())):
                avg = 0
                counter = 0
                feature1 = self.feature[feature_keys[i]]
                feature2 = self.feature[feature_keys[j]]
                similarity_matrix = torch.nn.functional.cosine_similarity(
                    feature1.unsqueeze(1), feature2.unsqueeze(0), dim=2)
                for sim in similarity_matrix.flatten():
                    avg += sim.item()
                    counter += 1
                    if sim.item() > standard:
                        self.similarity_list.append(feature_keys[i] + " : " +
                                                    feature_keys[j] +
                                                    f" avg: \t{sim.item()}")
                        break
                    elif sim.item() > 0.6:
                        self.relevance_list.append(feature_keys[i] + " : " +
                                                   feature_keys[j] +
                                                   f" avg: \t{sim.item()}")
                        break
                print(
                    f"{feature_keys[i]} : {feature_keys[j]} average : {avg/counter}"
                )


"""
main_folder
└──sub_folder = {pic1,pic2......}
└──sub_folder = {pic1,pic2......}
"""
