"""
utils/class_imbalance.py
=========================
EyePACS is heavily imbalanced: class 0 (No DR) typically makes up ~73% of
the dataset while class 4 (Proliferative DR) is often under 2%. Training
naively on this distribution biases the model toward predicting "No DR",
which is the worst possible failure mode for a screening tool (a false
negative on a sight-threatening case). This module provides two
complementary mitigations:

  1. compute_class_weights  - inverse-frequency class weights passed to
                               model.fit(..., class_weight=...)
  2. oversample_dataset     - tf.data-level rejection resampling that
                               rebalances the *stream* of examples the
                               model sees per epoch (useful in addition to,
                               or instead of, class weights)
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.utils.class_weight import compute_class_weight

import config


def compute_class_weights(labels: np.ndarray) -> dict:
    """
    Compute balanced class weights: weight_c = n_samples / (n_classes * n_c).

    Parameters
    ----------
    labels : array-like of int class labels (0-4)

    Returns
    -------
    dict {class_index: weight} suitable for `model.fit(class_weight=...)`
    """
    classes = np.arange(config.NUM_CLASSES)
    weights = compute_class_weight(class_weight="balanced", classes=classes, y=labels)
    class_weight_dict = {int(c): float(w) for c, w in zip(classes, weights)}
    return class_weight_dict


def class_distribution_report(labels: np.ndarray) -> pd.DataFrame:
    """Human-readable table of counts / percentages / derived weights per class."""
    counts = pd.Series(labels).value_counts().reindex(range(config.NUM_CLASSES), fill_value=0)
    weights = compute_class_weights(labels)
    df = pd.DataFrame({
        "class_index": counts.index,
        "class_name": [config.CLASS_LABELS[i] for i in counts.index],
        "count": counts.values,
        "percentage": (counts.values / counts.values.sum() * 100).round(2),
        "class_weight": [round(weights[i], 3) for i in counts.index],
    })
    return df


def oversample_dataset(file_paths: np.ndarray, labels: np.ndarray, target_dist: dict = None):
    """
    Build a rebalanced (path, label) tf.data.Dataset via per-class rejection
    resampling (tf.data.Dataset.rejection_resample), so minority classes
    (Severe, Proliferative DR) are seen more often per epoch without
    physically duplicating image files on disk.

    Parameters
    ----------
    file_paths : array of str image file paths
    labels     : array of int labels aligned with file_paths
    target_dist: optional dict {class: probability} summing to 1. Defaults
                 to a uniform distribution across all classes.

    Returns
    -------
    tf.data.Dataset yielding (path, label) pairs, rebalanced. Infinite
    stream (repeat()'d internally by rejection_resample) -- callers should
    `.take(steps_per_epoch)` when iterating for a bounded epoch.
    """
    if target_dist is None:
        target_dist = {c: 1.0 / config.NUM_CLASSES for c in range(config.NUM_CLASSES)}
    target_probs = [target_dist[c] for c in range(config.NUM_CLASSES)]

    ds = tf.data.Dataset.from_tensor_slices((file_paths, labels))
    ds = ds.shuffle(buffer_size=len(file_paths), seed=config.RANDOM_SEED, reshuffle_each_iteration=True)

    resampler = tf.data.Dataset.rejection_resample(
        class_func=lambda path, label: tf.cast(label, tf.int32),
        target_dist=target_probs,
        seed=config.RANDOM_SEED,
    )
    ds = ds.apply(resampler)
    # rejection_resample yields (class, (path, label)) tuples -> unwrap
    ds = ds.map(lambda _cls, example: example, num_parallel_calls=tf.data.AUTOTUNE)
    return ds
