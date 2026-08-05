"""
train.py
========
End-to-end training entry point for the EfficientNetB0 diabetic retinopathy
classifier.

Usage
-----
    python train.py                       # full two-phase training run
    python train.py --phase1-only         # feature-extraction phase only
    python train.py --baseline            # also train the comparison baseline CNN

Pipeline
--------
1. Load train/val manifests (run utils/prepare_dataset.py first if these
   don't exist yet).
2. Build tf.data pipelines (augmented train / clean val).
3. Compute class weights from the training distribution.
4. Phase 1: train the classification head with the backbone frozen.
5. Phase 2: unfreeze upper backbone layers, fine-tune at a low LR.
6. Save the best checkpoint (by validation macro recall) and the final model.
7. Persist merged training history + curves to results/.
"""

import argparse
import json
import os
import time

import tensorflow as tf

import config
from models.efficientnet_model import (
    build_efficientnet_model, compile_model, get_trainable_summary, unfreeze_for_fine_tuning,
)
from models.baseline_cnn import build_baseline_cnn, compile_baseline
from utils.class_imbalance import class_distribution_report, compute_class_weights
from utils.data_loader import build_dataset, get_labels_array
from utils.metrics import MacroRecallCallback, plot_training_curves


def build_callbacks(checkpoint_path: str, val_dataset: tf.data.Dataset, log_dir: str,
                     initial_value_threshold: float = None):
    """
    initial_value_threshold: pass the best monitored-metric value achieved so
    far (e.g. from a previous training phase) so ModelCheckpoint doesn't
    reset its notion of "best" to None/inf at the start of a new phase and
    overwrite a genuinely better earlier checkpoint with a worse one.
    """
    return [
        MacroRecallCallback(val_dataset),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path,
            monitor=config.MONITOR_METRIC,
            mode=config.MONITOR_MODE,
            save_best_only=True,
            initial_value_threshold=initial_value_threshold,
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor=config.MONITOR_METRIC,
            mode=config.MONITOR_MODE,
            patience=config.EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor=config.MONITOR_METRIC,
            mode=config.MONITOR_MODE,
            factor=config.REDUCE_LR_FACTOR,
            patience=config.REDUCE_LR_PATIENCE,
            min_lr=config.MIN_LR,
            verbose=1,
        ),
        tf.keras.callbacks.CSVLogger(os.path.join(log_dir, "training_log.csv"), append=True),
        tf.keras.callbacks.TensorBoard(log_dir=os.path.join(log_dir, "tensorboard")),
    ]


def merge_histories(*histories):
    merged = {}
    for h in histories:
        for k, v in h.history.items():
            merged.setdefault(k, []).extend(v)
    return merged


def train_efficientnet(phase1_only: bool = False):
    print("=" * 70)
    print("Loading data manifests ...")
    train_labels = get_labels_array(config.TRAIN_CSV)
    print(class_distribution_report(train_labels).to_string(index=False))

    train_ds = build_dataset(config.TRAIN_CSV, training=True, use_oversampling=config.USE_OVERSAMPLING)
    val_ds = build_dataset(config.VAL_CSV, training=False, cache=True)

    class_weights = compute_class_weights(train_labels) if config.USE_CLASS_WEIGHTS else None
    print(f"Class weights: {class_weights}")

    print("\nBuilding EfficientNetB0 model (Phase 1: frozen backbone) ...")
    model = build_efficientnet_model()
    model = compile_model(model, learning_rate=config.PHASE1_LR)
    print(get_trainable_summary(model))

    callbacks = build_callbacks(config.EFFICIENTNET_CKPT, val_ds, config.LOGS_DIR)

    print("\n--- PHASE 1: training classification head ---")
    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=config.PHASE1_EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks,
    )

    histories = [history1]

    if not phase1_only:
        print("\n--- PHASE 2: fine-tuning upper backbone layers ---")
        model = unfreeze_for_fine_tuning(model, config.FINE_TUNE_AT_LAYER)
        model = compile_model(model, learning_rate=config.PHASE2_LR)
        print(get_trainable_summary(model))

        phase1_best = max(history1.history.get("val_macro_recall", [0.0])) \
            if config.MONITOR_MODE == "max" else min(history1.history.get("val_macro_recall", [1.0]))
        callbacks = build_callbacks(config.EFFICIENTNET_CKPT, val_ds, config.LOGS_DIR,
                                     initial_value_threshold=phase1_best)
        history2 = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=config.PHASE1_EPOCHS + config.PHASE2_EPOCHS,
            initial_epoch=config.PHASE1_EPOCHS,
            class_weight=class_weights,
            callbacks=callbacks,
        )
        histories.append(history2)

    model.save(config.EFFICIENTNET_FINAL)
    print(f"\nFinal model saved to: {config.EFFICIENTNET_FINAL}")
    print(f"Best checkpoint (by {config.MONITOR_METRIC}) saved to: {config.EFFICIENTNET_CKPT}")

    merged_history = merge_histories(*histories)
    with open(os.path.join(config.LOGS_DIR, "efficientnet_history.json"), "w") as f:
        json.dump(merged_history, f, indent=2)

    plot_training_curves(merged_history, save_path=os.path.join(config.FIGURES_DIR, "efficientnet_training_curves.png"))

    return model, merged_history


def train_baseline():
    print("=" * 70)
    print("Training baseline CNN (from scratch, for comparison) ...")

    train_labels = get_labels_array(config.TRAIN_CSV)
    train_ds = build_dataset(config.TRAIN_CSV, training=True, use_oversampling=config.USE_OVERSAMPLING)
    val_ds = build_dataset(config.VAL_CSV, training=False, cache=True)
    class_weights = compute_class_weights(train_labels) if config.USE_CLASS_WEIGHTS else None

    model = build_baseline_cnn()
    model = compile_baseline(model, learning_rate=1e-3)

    total_epochs = config.PHASE1_EPOCHS + config.PHASE2_EPOCHS
    callbacks = build_callbacks(config.BASELINE_CKPT, val_ds, config.LOGS_DIR)

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=total_epochs,
        class_weight=class_weights,
        callbacks=callbacks,
    )

    with open(os.path.join(config.LOGS_DIR, "baseline_history.json"), "w") as f:
        json.dump(history.history, f, indent=2)

    plot_training_curves(history.history, save_path=os.path.join(config.FIGURES_DIR, "baseline_training_curves.png"))
    print(f"Baseline model checkpoint saved to: {config.BASELINE_CKPT}")
    return model, history.history


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the DR classification models.")
    parser.add_argument("--phase1-only", action="store_true", help="Only run Phase 1 (frozen backbone).")
    parser.add_argument("--baseline", action="store_true", help="Also train the comparison baseline CNN.")
    parser.add_argument("--baseline-only", action="store_true", help="Train only the baseline CNN.")
    args = parser.parse_args()

    start = time.time()

    if args.baseline_only:
        train_baseline()
    else:
        train_efficientnet(phase1_only=args.phase1_only)
        if args.baseline:
            train_baseline()

    print(f"\nTotal training time: {(time.time() - start) / 60:.1f} minutes")
