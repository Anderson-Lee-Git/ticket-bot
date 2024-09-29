import os

import torch
from torch.utils.data import Dataset
import pandas as pd
from PIL import Image
# from torchvision import transforms
from transformers import AutoImageProcessor

image_processor = AutoImageProcessor.from_pretrained("apple/mobilevitv2-1.0-imagenet1k-256")


class CaptchaDataset(Dataset):
    def __init__(self, data_dir, split):
        """
        Args:
            data_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.data_dir = data_dir
        self.split = split
        # self.transform = transforms.Compose([
        #     transforms.Resize((224, 224)),
        #     transforms.ToTensor(),
        #     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        # ])
        self.transform = None
        self.data = self._load_data()

    def _load_metadata(self):
        return pd.read_csv(f'meta/{self.split}.csv')

    def _load_data(self):
        # Implement data loading logic here
        # For example, you can list all files in the directory
        # and read them into memory
        md = self._load_metadata()
        data = []
        for i in range(len(md)):
            img_name = md.iloc[i, 0] + '.png'
            img_path = os.path.join(self.data_dir, img_name)
            image = Image.open(img_path)
            target = self.text_to_encoding(md.iloc[i, 0])
            data.append((image, target))
        return data

    def text_to_encoding(self, text):
        # text is a four-character string with only lowercase letters
        # encoding is a 4x26 tensor where each row is a one-hot encoding of the character
        # where the entry is 1 if the character is at the position
        encoding = torch.zeros(4, 26)
        for i, char in enumerate(text):
            encoding[i, ord(char) - ord('a')] = 1
        return encoding.flatten(0)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        image, target = self.data[idx]
        if self.transform:
            image = self.transform(image)
        return image, target


# Custom collate function that uses AutoImageProcessor to preprocess the images
def collate_fn(batch):
    images, targets = list(zip(*batch))
    inputs = image_processor(images, return_tensors="pt")
    return inputs, torch.stack(targets)


def get_datasets():
    train_dataset = CaptchaDataset(data_dir='data', split='train')
    val_dataset = CaptchaDataset(data_dir='data', split='val')
    test_dataset = CaptchaDataset(data_dir='data', split='test')
    return train_dataset, val_dataset, test_dataset
