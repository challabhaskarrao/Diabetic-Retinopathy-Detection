"""
utils/data_loader.py
=====================
Builds tf.data.Dataset pipelines from CSV manifests (image, level) pointing
at EyePACS fundus images on disk.

Design notes
------------
* Heavy, hard-to-vectorize preprocessing (Ben Graham local-average
  subtraction, denoising, quality checks) is done with OpenCV via
  `tf.numpy_function`, wrapped once per image.
* Augmentation (utils/augmentation.py) is applied only to the training
  split, in-graph, batched (faster than per-image).
* The final step applies `tf.keras.applications.efficientnet.preprocess_input`
  so pixel scaling exactly matches what the ImageNet-pretrained backbone
  expects.
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

import config
from utils.preprocessing import preprocess_image


# --------------------------------------------------------------------------
# Manifest preparation (run once, offline)
# --------------------------------------------------------------------------
def create_splits(source_csv: str, image_col: str = "image", label_col: str = "level",
                   image_dir: str = None, extension: str = None):
    """
    Read the raw EyePACS trainLabels.csv-style manifest and produce
    stratified train/val/test CSVs with an absolute `filepath` column, saved
    to config.TRAIN_CSV / VAL_CSV / TEST_CSV.

    Stratification keeps the (heavily skewed) class proportions consistent
    across splits so validation/test metrics are representative.
    """
    image_dir = image_dir or config.RAW_IMAGE_DIR
    extension = extension or config.IMAGE_EXTENSION

    df = pd.read_csv(source_csv)
    df = df.rename(columns={image_col: "image", label_col: "level"})
    df["filepath"] = df["image"].apply(
        lambda name: name if name.endswith(extension) else f"{name}{extension}"
    )
    df["filepath"] = df["filepath"].apply(lambda fname: f"{image_dir}/{fname}")

    train_df, temp_df = train_test_split(
        df, test_size=(config.VAL_SPLIT + config.TEST_SPLIT),
        stratify=df["level"], random_state=config.RANDOM_SEED,
    )
    relative_test_size = config.TEST_SPLIT / (config.VAL_SPLIT + config.TEST_SPLIT)
    val_df, test_df = train_test_split(
        temp_df, test_size=relative_test_size,
        stratify=temp_df["level"], random_state=config.RANDOM_SEED,
    )

    train_df.to_csv(config.TRAIN_CSV, index=False)
    val_df.to_csv(config.VAL_CSV, index=False)
    test_df.to_csv(config.TEST_CSV, index=False)

    return train_df, val_df, test_df


def load_manifest(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    assert "filepath" in df.columns and "level" in df.columns, (
        "Manifest CSV must contain 'filepath' and 'level' columns. "
        "Run utils.data_loader.create_splits() first."
    )
    return df


# --------------------------------------------------------------------------
# tf.data pipeline
# --------------------------------------------------------------------------
def _numpy_preprocess(path_tensor):
    """tf.numpy_function wrapper around the OpenCV preprocessing pipeline."""
    path = path_tensor.numpy().decode("utf-8")
    image = preprocess_image(path)                 # float32 [0,1], IMG_SIZE x IMG_SIZE x 3
    image = (image * 255.0).astype(np.float32)      # back to 0-255 for Keras augmentation/preprocess_input
    return image


def _load_and_preprocess(path, label):
    image = tf.py_function(func=_numpy_preprocess, inp=[path], Tout=tf.float32)
    image.set_shape([config.IMG_SIZE, config.IMG_SIZE, 3])
    label = tf.cast(label, tf.int32)
    return image, label


def _apply_efficientnet_scaling(image, label):
    image = tf.keras.applications.efficientnet.preprocess_input(image)
    return image, label


def _augment(image, label):
    from utils.augmentation import augment_batch
    image = augment_batch(tf.expand_dims(image, 0), training=True)[0]
    return image, label


def build_dataset(csv_path: str, batch_size: int = None, training: bool = False,
                   use_oversampling: bool = False, cache: bool = False) -> tf.data.Dataset:
    """
    Build a batched, prefetched tf.data.Dataset from a manifest CSV.

    Parameters
    ----------
    csv_path : path to a manifest produced by create_splits()
    batch_size : defaults to config.BATCH_SIZE
    training : if True, shuffles and applies augmentation
    use_oversampling : if True (and training), rebalance classes via
        utils.class_imbalance.oversample_dataset instead of natural sampling
    cache : cache decoded/preprocessed images in memory after first epoch
        (only recommended for small/val/test sets - full training sets
        rarely fit in RAM)
    """
    batch_size = batch_size or config.BATCH_SIZE
    df = load_manifest(csv_path)
    paths = df["filepath"].values
    labels = df["level"].values.astype(np.int32)

    if training and use_oversampling:
        from utils.class_imbalance import oversample_dataset
        ds = oversample_dataset(paths, labels, target_dist=config.OVERSAMPLE_TARGET_DIST)
        steps_per_epoch = len(paths) // batch_size
        ds = ds.take(steps_per_epoch * batch_size)
    else:
        ds = tf.data.Dataset.from_tensor_slices((paths, labels))
        if training:
            ds = ds.shuffle(buffer_size=min(len(paths), config.SHUFFLE_BUFFER),
                             seed=config.RANDOM_SEED, reshuffle_each_iteration=True)

    ds = ds.map(_load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)

    if cache:
        ds = ds.cache()

    if training:
        ds = ds.batch(batch_size)
        ds = ds.map(lambda imgs, lbls: (augment_batch_wrapper(imgs), lbls),
                    num_parallel_calls=tf.data.AUTOTUNE)
    else:
        ds = ds.batch(batch_size)

    ds = ds.map(_apply_efficientnet_scaling, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds


def augment_batch_wrapper(images):
    from utils.augmentation import augment_batch
    return augment_batch(images, training=True)


def get_labels_array(csv_path: str) -> np.ndarray:
    """Convenience accessor used by class_imbalance.py and evaluate.py."""
    return load_manifest(csv_path)["level"].values.astype(np.int32)
