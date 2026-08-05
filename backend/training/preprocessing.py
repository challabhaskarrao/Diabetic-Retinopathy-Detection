import cv2
import numpy as np
from PIL import Image

def crop_image_from_gray(img, tol=7):
    """
    Crop the black borders of a retinal image.
    Works by finding the bounding box of the non-black pixels.
    """
    if img.ndim == 2:
        mask = img > tol
        return img[np.ix_(mask.any(1), mask.any(0))]
    elif img.ndim == 3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mask = gray_img > tol
        check_shape = img[:, :, 0][np.ix_(mask.any(1), mask.any(0))].shape[0]
        if check_shape == 0:
            return img # image is too dark, return original
        else:
            img1 = img[:, :, 0][np.ix_(mask.any(1), mask.any(0))]
            img2 = img[:, :, 1][np.ix_(mask.any(1), mask.any(0))]
            img3 = img[:, :, 2][np.ix_(mask.any(1), mask.any(0))]
            img = np.stack([img1, img2, img3], axis=-1)
        return img
    return img

def apply_clahe(img):
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    to enhance the contrast of the retinal image.
    """
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    return enhanced_img

def preprocess_image(image_path, target_size=(300, 300)):
    """
    Full preprocessing pipeline:
    1. Read image
    2. Crop black borders
    3. Resize
    4. Apply CLAHE
    """
    # Read image using OpenCV and convert to RGB
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Unable to read image at {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 1. Crop black borders
    img = crop_image_from_gray(img)
    
    # 2. Resize
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    
    # 3. Apply CLAHE for contrast enhancement
    img = apply_clahe(img)
    
    return img
