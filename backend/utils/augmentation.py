"""
utils/augmentation.py
======================
Training-time data augmentation for retinal fundus images.

Implemented with tf.keras preprocessing layers (rather than the older
ImageDataGenerator) so augmentation:
  * runs on-GPU as part of the tf.data pipeline (fast),
  * is automatically disabled at inference time (`training=False`),
  * is serializable if ever bundled into the model itself.

Fundus-specific note: unlike natural images, retinal photographs are NOT
vertically-flip invariant in a clinically meaningful way for laterality-
sensitive lesions in some protocols, so by default we only enable
horizontal flip. Rotation is kept moderate since fundus cameras already
center the optic disc/macula fairly consistently.
"""

import tensorflow as tf
from tensorflow.keras import layers

import config


def build_augmentation_pipeline() -> tf.keras.Sequential:
    """
    Returns a Keras Sequential of augmentation layers implementing:
      - random rotation
      - random horizontal flip
      - random zoom
      - random brightness adjustment
      - random contrast (small extra touch to better simulate camera variability)
    """
    aug_layers = []

    if config.HORIZONTAL_FLIP:
        aug_layers.append(layers.RandomFlip("horizontal", name="random_flip"))

    aug_layers.append(layers.RandomRotation(config.ROTATION_RANGE, fill_mode="constant",
                                             fill_value=0.0, name="random_rotation"))
    aug_layers.append(layers.RandomZoom(height_factor=config.ZOOM_RANGE,
                                         width_factor=config.ZOOM_RANGE,
                                         fill_mode="constant", fill_value=0.0,
                                         name="random_zoom"))
    aug_layers.append(layers.RandomBrightness(factor=config.BRIGHTNESS_RANGE,
                                               value_range=(0, 255), name="random_brightness"))
    aug_layers.append(layers.RandomContrast(factor=config.CONTRAST_RANGE, name="random_contrast"))

    return tf.keras.Sequential(aug_layers, name="augmentation_pipeline")


# A module-level singleton so the same augmentation graph is reused everywhere
augmentation_pipeline = build_augmentation_pipeline()


def augment_batch(images: tf.Tensor, training: bool = True) -> tf.Tensor:
    """Apply the augmentation pipeline to a batch of images (0-255 float32)."""
    return augmentation_pipeline(images, training=training)


def preview_augmentations(image: "np.ndarray", n: int = 6):
    """
    Utility for notebooks: given a single 0-255 float32/uint8 image, return
    `n` augmented variants for visual inspection (e.g. in the training notebook's
    EDA section) to sanity-check the augmentation ranges look clinically reasonable.
    """
    import numpy as np
    image = tf.convert_to_tensor(image, dtype=tf.float32)
    batch = tf.stack([image] * n, axis=0)
    augmented = augmentation_pipeline(batch, training=True)
    return np.clip(augmented.numpy(), 0, 255).astype(np.uint8)
