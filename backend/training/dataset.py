import os
import glob
from pathlib import Path
from PIL import Image
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split

from .preprocessing import preprocess_image
from .augmentations import get_train_transforms, get_val_transforms
from .config import config

class RetinalDataset(Dataset):
    """
    Custom Dataset for Diabetic Retinopathy.
    Supports reading from directories organized by class (0, 1, 2, 3, 4)
    or from a CSV file containing image paths and labels.
    """
    def __init__(self, image_paths, labels, transforms=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transforms = transforms

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        
        # Apply preprocessing (crop borders, CLAHE, etc.)
        try:
            image = preprocess_image(img_path, target_size=(config.IMAGE_SIZE, config.IMAGE_SIZE))
        except Exception as e:
            # Fallback if image is corrupted or missing
            image = np.zeros((config.IMAGE_SIZE, config.IMAGE_SIZE, 3), dtype=np.uint8)
            print(f"Warning: Failed to load {img_path}. Using empty image. Error: {e}")

        if self.transforms:
            # Albumentations expects a numpy array
            augmented = self.transforms(image=image)
            image = augmented['image']
        else:
            # Default to tensor conversion if no transforms provided
            image = torch.from_numpy(image.transpose((2, 0, 1))).float() / 255.0

        return image, torch.tensor(label, dtype=torch.long)

def parse_dataset_directory(data_dir: Path):
    """
    Parses a directory structure where subfolders are class labels (0 to 4).
    E.g., data/0/img1.jpg, data/1/img2.jpg, etc.
    """
    image_paths = []
    labels = []
    
    for class_id in range(config.NUM_CLASSES):
        class_dir = data_dir / str(class_id)
        if class_dir.exists():
            for img_path in class_dir.glob("*.[jp][pn]*[g]"): # Matches jpg, png, jpeg
                image_paths.append(str(img_path))
                labels.append(class_id)
                
    return image_paths, labels

def create_dataloaders(data_dir=None, test_size=0.2, val_size=0.1, batch_size=None):
    """
    Creates Train, Validation, and Test dataloaders.
    Automatically reads folders and labels.
    """
    if data_dir is None:
        data_dir = config.DATA_DIR
    if batch_size is None:
        batch_size = config.BATCH_SIZE
        
    image_paths, labels = parse_dataset_directory(Path(data_dir))
    
    if len(image_paths) == 0:
        raise ValueError(f"No images found in {data_dir}. Ensure folders 0, 1, 2, 3, 4 exist.")

    # Split into train+val and test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        image_paths, labels, test_size=test_size, stratify=labels, random_state=42
    )
    
    # Split train+val into train and val
    val_ratio = val_size / (1.0 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio, stratify=y_train_val, random_state=42
    )
    
    print(f"Dataset split: {len(X_train)} Train, {len(X_val)} Val, {len(X_test)} Test")
    
    # Create datasets
    train_dataset = RetinalDataset(X_train, y_train, transforms=get_train_transforms(config.IMAGE_SIZE))
    val_dataset = RetinalDataset(X_val, y_val, transforms=get_val_transforms(config.IMAGE_SIZE))
    test_dataset = RetinalDataset(X_test, y_test, transforms=get_val_transforms(config.IMAGE_SIZE))
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=config.NUM_WORKERS, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=config.NUM_WORKERS, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=config.NUM_WORKERS, pin_memory=True)
    
    return train_loader, val_loader, test_loader
