import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data import Dataset

from PIL import Image
import os

""" Model structure deciding which action to take attack/expore """
class ClassificationCNN(nn.Module):
    def __init__(self):
        super(ClassificationCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 45 * 80, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 64 * 45 * 80)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x = torch.sigmoid(x)
        return x

class ClassificationCNN_type2(nn.Module):
    def __init__(self):
        super(ClassificationCNN_type2, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 45 * 80, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32,2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 64 * 45 * 80)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        x = torch.sigmoid(x)
        return x



""" Model structure for mouse x,y predicitions """
class MousePositionCNN(nn.Module):
    def __init__(self):
        super(MousePositionCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 45 * 80, 512)  # Adjust dimensions based on image size and pooling
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 2)  # Output layer with 2 values (x, y)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 64 * 45 * 80)  # Flatten the tensor
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

""" Normalization of inputted images to tensors with width 640 and height 360 pixels """
transform_preset = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((360, 640)), ###############
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

""" Creates a class used for dataloader"""
class ClassificationDataset(Dataset):
    """
    :param folder_paths: list of folder paths where images and .csv dataframe is located
    :param transform: Properties for normalization of input images
    """
    def __init__(self, folder_paths: list[str], transform=transform_preset):
        self.folder_path_list = [folder_path for folder_path in folder_paths]
        self.transform = transform
        self.images = []
        self.labels = []
        self.class_mapping = {
            'attack_img': [1, 0],
            'explore_img': [0, 1]
        }
        self.load_dataset()
    """ 
    The main folder has 2 subfolders 'attack_img':[1, 0] or 'explore_img': [0, 1]. 
    All images are resized to 640x360 and transformed to tensors.
    """
    def load_dataset(self):
        for folder_path in self.folder_path_list:
            for folder_name in ['attack_img', 'explore_img']:
                folder_full_path = os.path.join(folder_path, folder_name)
                class_label = self.class_mapping[folder_name]
                for filename in os.listdir(folder_full_path):
                    if filename.endswith(".jpg"):
                        img_path = os.path.join(folder_full_path, filename)

                        self.images.append(img_path)
                        self.labels.append(class_label)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        img = Image.open(img_path).convert('RGB')
        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        if self.transform:
            img = self.transform(img)

        return img, label


