import cv2
import numpy as np
from PIL import Image

class ImageQualityAssessor:
    def __init__(self, blur_threshold=100.0, brightness_low=40, brightness_high=220):
        self.blur_threshold = blur_threshold
        self.brightness_low = brightness_low
        self.brightness_high = brightness_high

    def _get_blur_score(self, gray_img):
        """
        Calculates the variance of the Laplacian.
        A lower variance indicates a blurred image.
        """
        return cv2.Laplacian(gray_img, cv2.CV_64F).var()

    def _get_brightness_score(self, hsv_img):
        """
        Calculates the mean brightness from the V channel in HSV.
        """
        return np.mean(hsv_img[:, :, 2])

    def assess_quality(self, image: np.ndarray):
        """
        Evaluates retinal image quality.
        Returns a tuple: (is_pass: bool, reason: str, details: dict)
        """
        if image is None or image.size == 0:
            return False, "Invalid image format.", {}

        # Resize for faster processing if image is huge, keeping aspect ratio
        h, w = image.shape[:2]
        if h * w > 1000 * 1000:
            scale = 1000.0 / max(h, w)
            proc_image = cv2.resize(image, (int(w * scale), int(h * scale)))
        else:
            proc_image = image

        # Convert to Grayscale and HSV
        gray = cv2.cvtColor(proc_image, cv2.COLOR_RGB2GRAY)
        hsv = cv2.cvtColor(proc_image, cv2.COLOR_RGB2HSV)

        # Calculate scores
        blur_score = self._get_blur_score(gray)
        brightness_score = self._get_brightness_score(hsv)

        details = {
            "blur_score": float(blur_score),
            "brightness_score": float(brightness_score),
            "resolution": f"{w}x{h}"
        }

        # Check conditions
        if blur_score < self.blur_threshold:
            return False, "Image quality insufficient for reliable AI diagnosis (Too blurred).", details
        
        if brightness_score < self.brightness_low:
            return False, "Image quality insufficient for reliable AI diagnosis (Too dark/Low brightness).", details
            
        if brightness_score > self.brightness_high:
            return False, "Image quality insufficient for reliable AI diagnosis (Overexposed).", details

        if w < 300 or h < 300:
            return False, "Image quality insufficient for reliable AI diagnosis (Incorrect resolution).", details

        return True, "Image quality is sufficient.", details
