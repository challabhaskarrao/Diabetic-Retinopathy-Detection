"""
tests/test_pipeline.py
=======================
Lightweight smoke tests that exercise every module end-to-end on
synthetic (random-noise) images, WITHOUT requiring the real EyePACS
dataset. Useful for:
  * Verifying a fresh environment/installation before a long training run.
  * CI (these run in well under a minute on CPU).
  * Confirming the model architecture, Grad-CAM, and metrics code are all
    wired together correctly.

Run with:
    pytest tests/test_pipeline.py -v
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config


def make_dummy_fundus_image(size=512, seed=0):
    """A synthetic 'fundus-like' image: a bright circle on a black background,
    similar enough in structure to a real fundus photo for pipeline testing."""
    rng = np.random.RandomState(seed)
    img = np.zeros((size, size, 3), dtype=np.uint8)
    yy, xx = np.ogrid[:size, :size]
    center = size // 2
    radius = int(size * 0.42)
    mask = (yy - center) ** 2 + (xx - center) ** 2 <= radius ** 2
    img[mask] = rng.randint(60, 200, size=(mask.sum(), 3)).astype(np.uint8)
    return img


class TestPreprocessing:
    def test_full_pipeline_shape_and_range(self):
        from utils.preprocessing import preprocess_image
        img = make_dummy_fundus_image()
        out = preprocess_image(img)
        assert out.shape == (config.IMG_SIZE, config.IMG_SIZE, 3)
        assert out.dtype == np.float32
        assert 0.0 <= out.min() and out.max() <= 1.0

    def test_quality_assessment_flags_dark_image(self):
        from utils.preprocessing import assess_image_quality
        black_image = np.zeros((256, 256, 3), dtype=np.uint8)
        quality = assess_image_quality(black_image)
        assert quality["is_usable"] is False

    def test_quality_assessment_passes_normal_image(self):
        from utils.preprocessing import assess_image_quality
        img = make_dummy_fundus_image()
        quality = assess_image_quality(img)
        assert "is_usable" in quality

    def test_ben_graham_preprocess_output_shape(self):
        from utils.preprocessing import ben_graham_preprocess
        img = make_dummy_fundus_image()
        out = ben_graham_preprocess(img)
        assert out.shape == img.shape
        assert out.dtype == np.uint8


class TestAugmentation:
    def test_augmentation_pipeline_preserves_shape(self):
        from utils.augmentation import preview_augmentations
        img = make_dummy_fundus_image(size=config.IMG_SIZE).astype(np.float32)
        augmented = preview_augmentations(img, n=4)
        assert augmented.shape == (4, config.IMG_SIZE, config.IMG_SIZE, 3)


class TestClassImbalance:
    def test_class_weights_sum_reasonable(self):
        from utils.class_imbalance import compute_class_weights
        labels = np.array([0] * 730 + [1] * 70 + [2] * 150 + [3] * 25 + [4] * 20)
        weights = compute_class_weights(labels)
        assert len(weights) == config.NUM_CLASSES
        # Minority classes should receive larger weights than the majority class
        assert weights[4] > weights[0]

    def test_class_distribution_report_shape(self):
        from utils.class_imbalance import class_distribution_report
        labels = np.random.randint(0, config.NUM_CLASSES, size=200)
        df = class_distribution_report(labels)
        assert len(df) == config.NUM_CLASSES


@pytest.mark.slow
class TestModels:
    def test_baseline_cnn_forward_pass(self):
        import tensorflow as tf
        from models.baseline_cnn import build_baseline_cnn
        model = build_baseline_cnn()
        dummy_batch = tf.random.uniform((2, *config.IMG_SHAPE))
        preds = model(dummy_batch, training=False)
        assert preds.shape == (2, config.NUM_CLASSES)
        assert np.allclose(np.sum(preds.numpy(), axis=1), 1.0, atol=1e-4)

    def test_efficientnet_forward_pass_and_freeze_state(self):
        import tensorflow as tf
        from models.efficientnet_model import build_efficientnet_model, get_backbone_layers
        model = build_efficientnet_model()
        backbone_layers = get_backbone_layers(model)
        assert all(not layer.trainable for layer in backbone_layers)

        dummy_batch = tf.random.uniform((1, *config.IMG_SHAPE), maxval=255.0)
        preds = model(dummy_batch, training=False)
        assert preds.shape == (1, config.NUM_CLASSES)

    def test_unfreeze_for_fine_tuning_changes_trainable_layers(self):
        from models.efficientnet_model import (
            build_efficientnet_model, get_backbone_layers, unfreeze_for_fine_tuning,
        )
        model = build_efficientnet_model()
        model = unfreeze_for_fine_tuning(model, fine_tune_at=200)
        backbone_layers = get_backbone_layers(model)
        trainable_count = sum(1 for l in backbone_layers if l.trainable)
        assert trainable_count > 0
        assert trainable_count < len(backbone_layers)  # only the top layers should be trainable


@pytest.mark.slow
class TestGradCAM:
    def test_gradcam_heatmap_and_overlay_shapes(self):
        import tensorflow as tf
        from models.efficientnet_model import build_efficientnet_model
        from gradcam.gradcam import GradCAM

        model = build_efficientnet_model()
        cam = GradCAM(model, layer_name=config.GRADCAM_LAYER_NAME)

        dummy_batch = tf.random.uniform((1, *config.IMG_SHAPE), maxval=255.0).numpy()
        heatmap, class_idx = cam.compute_heatmap(dummy_batch)
        assert 0 <= class_idx < config.NUM_CLASSES
        assert heatmap.ndim == 2
        assert heatmap.min() >= 0.0 and heatmap.max() <= 1.0 + 1e-5

        original = make_dummy_fundus_image(size=300)
        overlay = cam.overlay_heatmap(original, heatmap)
        assert overlay.shape == original.shape
        assert overlay.dtype == np.uint8


class TestMetrics:
    def test_compute_full_metrics_keys(self):
        from utils.metrics import compute_full_metrics
        rng = np.random.RandomState(0)
        y_true = rng.randint(0, config.NUM_CLASSES, size=100)
        y_pred = rng.randint(0, config.NUM_CLASSES, size=100)
        y_proba = np.eye(config.NUM_CLASSES)[y_pred]

        results = compute_full_metrics(y_true, y_pred, y_proba)
        for key in ["accuracy", "precision_macro", "recall_macro", "f1_macro",
                    "confusion_matrix", "classification_report", "per_class"]:
            assert key in results
        assert results["confusion_matrix"].shape == (config.NUM_CLASSES, config.NUM_CLASSES)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
