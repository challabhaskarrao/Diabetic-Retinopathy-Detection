"""
utils/preprocessing.py
=======================
Image-level preprocessing for retinal fundus photographs.

Functions here operate on single images (numpy arrays, uint8, BGR or RGB as
noted per-function) and are used both by the offline dataset-preparation
script and by the online inference path, so training and serving stay
consistent.

Pipeline used throughout the project:
    1. load_image            -> read from disk, RGB uint8
    2. assess_image_quality  -> flag blurry / too-dark / badly-cropped images
    3. crop_to_content       -> remove black fundus borders
    4. denoise_image         -> mild edge-preserving denoising (optional)
    5. ben_graham_preprocess -> local-average subtraction + contrast boost
       (the technique used by the winning EyePACS Kaggle solution, 2015)
    6. resize_image           -> 224x224 for EfficientNetB0
    7. normalize_image        -> scale to [0, 1] float32
"""

import cv2
import numpy as np

import config


# --------------------------------------------------------------------------
# I/O
# --------------------------------------------------------------------------
def load_image(path: str) -> np.ndarray:
    """Load an image from disk and return it as RGB uint8."""
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image at: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


# --------------------------------------------------------------------------
# Quality assessment
# --------------------------------------------------------------------------
def assess_image_quality(image: np.ndarray) -> dict:
    """
    Heuristic quality check for a fundus photograph.

    Returns a dict with:
        is_usable (bool), blur_score (float), dark_fraction (float), reason (str)

    Two common EyePACS quality issues are targeted:
      * Out-of-focus / motion-blurred captures -> low Laplacian variance.
      * Severely under-illuminated or mostly-black captures (bad camera
        alignment) -> high fraction of near-zero pixels.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    dark_fraction = float(np.mean(gray < 10))

    reasons = []
    if blur_score < config.BLUR_VARIANCE_THRESHOLD:
        reasons.append("low_sharpness")
    if dark_fraction > config.DARK_PIXEL_FRACTION_THRESHOLD:
        reasons.append("mostly_dark_or_poor_crop")

    return {
        "is_usable": len(reasons) == 0,
        "blur_score": blur_score,
        "dark_fraction": dark_fraction,
        "reason": ",".join(reasons) if reasons else "ok",
    }


# --------------------------------------------------------------------------
# Cropping
# --------------------------------------------------------------------------
def crop_to_content(image: np.ndarray, threshold: int = 10) -> np.ndarray:
    """
    Crop away the black background surrounding the circular fundus image.
    Falls back to the original image if the detected content is too small
    (guards against over-cropping on unusually dark but valid photos).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    mask = gray > threshold

    if mask.sum() < 0.05 * mask.size:
        return image

    coords = np.argwhere(mask)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    cropped = image[y0:y1, x0:x1]
    if cropped.shape[0] < 32 or cropped.shape[1] < 32:
        return image
    return cropped


# --------------------------------------------------------------------------
# Denoising
# --------------------------------------------------------------------------
def denoise_image(image: np.ndarray) -> np.ndarray:
    """
    Mild edge-preserving denoising. Uses a fast Non-Local-Means denoiser,
    tuned conservatively so fine vascular / haemorrhage detail (which is
    diagnostically important) is not smoothed away.
    """
    return cv2.fastNlMeansDenoisingColored(image, None, h=4, hColor=4,
                                            templateWindowSize=7, searchWindowSize=21)


# --------------------------------------------------------------------------
# Ben Graham preprocessing (Kaggle DR 1st-place technique, 2015)
# --------------------------------------------------------------------------
def ben_graham_preprocess(image: np.ndarray, sigma_fraction: float = 10.0) -> np.ndarray:
    """
    Subtract a heavily Gaussian-blurred version of the image from itself and
    re-centre at mid-gray. This suppresses uneven illumination between scans
    (a major source of domain shift in EyePACS, which was captured across
    many different clinics/cameras) and dramatically boosts the visibility
    of microaneurysms, haemorrhages, and exudates.

        result = 4 * image - 4 * GaussianBlur(image, sigma) + 128
    """
    height = image.shape[0]
    sigma = max(height / sigma_fraction, 1.0)
    blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=sigma)
    result = cv2.addWeighted(image, 4, blurred, -4, 128)
    return np.clip(result, 0, 255).astype(np.uint8)


# --------------------------------------------------------------------------
# Resize / normalize
# --------------------------------------------------------------------------
def resize_image(image: np.ndarray, size: int = None) -> np.ndarray:
    size = size or config.IMG_SIZE
    return cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Scale uint8 [0, 255] image to float32 [0, 1]."""
    return image.astype(np.float32) / 255.0


# --------------------------------------------------------------------------
# Full pipeline
# --------------------------------------------------------------------------
def preprocess_image(path_or_array, return_quality: bool = False):
    """
    Run the complete preprocessing pipeline used for both training-data
    preparation and single-image inference.

    Parameters
    ----------
    path_or_array : str or np.ndarray
        Path to an image on disk, or an already-loaded RGB uint8 array.
    return_quality : bool
        If True, also return the quality-assessment dict.

    Returns
    -------
    np.ndarray float32, shape (IMG_SIZE, IMG_SIZE, 3), values in [0, 1]
    (and optionally the quality dict)
    """
    image = load_image(path_or_array) if isinstance(path_or_array, str) else path_or_array

    quality = assess_image_quality(image)

    image = crop_to_content(image)

    if config.APPLY_DENOISING:
        image = denoise_image(image)

    if config.APPLY_BEN_GRAHAM_PREPROCESSING:
        image = ben_graham_preprocess(image)

    image = resize_image(image)
    image = normalize_image(image)

    if return_quality:
        return image, quality
    return image
