from torchvision import models, transforms
from PIL import Image
import torch
import os

standar = 0.9
path = "D:\\test_folder"
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


class ImageReader:
    def __init__(self):
        self.sub_folder_list = []
        self.similarity_list = []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT).to(
            self.device
        )
        self.preprocess = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
        self.model.eval()
        self.scan_folder()

    def scan_folder(self):
        self.sub_folder_list = os.listdir(path)
        if len(self.sub_folder_list) == 0:
            return False
        return True

    def scan_sub_folder_pic(self, sub_folder_name):
        full_path = os.path.join(path, sub_folder_name)
        sub_folder_images_path = []
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            if os.path.isfile(file_path) and file.split(".")[-1].lower() in image_types:
                sub_folder_images_path.append(file_path)
        return sub_folder_images_path

    def extract_features(self, image_paths):
        images = []
        for image_path in image_paths:
            images.append(self.preprocess(Image.open(image_path).convert("RGB")))
        images = torch.stack(images).to(self.device)
        with torch.no_grad():
            features = self.model(images)
        return features

    def execute(self):  # features = {"sub_folder_name":feature_list}
        features = {}
        for sub_folder in self.sub_folder_list:
            print(f'extracting "{sub_folder}" content')
            image_paths = self.scan_sub_folder_pic(sub_folder)
            features[sub_folder] = self.extract_features(image_paths)
        feature_keys = list(features.keys())

        for i in range(len(features.values())):
            for j in range(i + 1, len(features.values())):
                feature1 = features[feature_keys[i]]
                feature2 = features[feature_keys[j]]
                similarity_matrix = torch.nn.functional.cosine_similarity(
                    feature1.unsqueeze(1), feature2.unsqueeze(0), dim=2
                )
                for sim in similarity_matrix.flatten():
                    if sim.item() > standar:
                        self.similarity_list.append(
                            feature_keys[i] + ":" + feature_keys[j]
                        )
                        break


if __name__ == "__main__":
    img_reader = ImageReader()
    img_reader.execute()
    if len(img_reader.similarity_list) != 0:
        print("find similarit!!!\n")
        for i in img_reader.similarity_list:
            print(i)
    else:
        print("pass!!")


"""
main_folder
└──sub_folder = {pic1,pic2......}
└──sub_folder = {pic1,pic2......}
"""
