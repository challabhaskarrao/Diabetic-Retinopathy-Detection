import albumentations as A
from albumentations.pytorch import ToTensorV2

def get_train_transforms(image_size=300):
    """
    Data augmentations for the training set.
    Includes Random Rotation, Horizontal Flip, Brightness, Contrast, 
    Random Crop, Zoom (via Scale), Color Jitter.
    STRICTLY excludes Vertical Flip as per requirements.
    """
    return A.Compose([
        A.RandomResizedCrop(height=image_size, width=image_size, scale=(0.8, 1.0), p=1.0), # Zoom / Crop
        A.HorizontalFlip(p=0.5),
        # NO VerticalFlip
        A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=15, p=0.5), # Rotation
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5), # Brightness & Contrast
        A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.3), # Color Jitter
        A.Normalize(
            mean=[0.485, 0.456, 0.406], # ImageNet mean
            std=[0.229, 0.224, 0.225],  # ImageNet std
            max_pixel_value=255.0,
            p=1.0
        ),
        ToTensorV2()
    ])

def get_val_transforms(image_size=300):
    """
    Transforms for validation and testing sets (only resize and normalize).
    """
    return A.Compose([
        A.Resize(height=image_size, width=image_size, p=1.0),
        A.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
            max_pixel_value=255.0,
            p=1.0
        ),
        ToTensorV2()
    ])
