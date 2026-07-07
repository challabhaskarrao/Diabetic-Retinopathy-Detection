"""
utils/metrics.py
=================
Evaluation utilities shared by training (as a Keras callback) and the
standalone evaluate.py script.

Includes:
  * MacroRecallCallback  - computes macro-averaged recall on the validation
                            set at the end of every epoch. Used to drive
                            EarlyStopping / ModelCheckpoint, because for a
                            medical screening tool, missing a true DR case
                            (false negative) is far costlier than a false
                            alarm - plain accuracy does not capture that.
  * compute_full_metrics - accuracy / precision / recall / F1 (per-class,
                            macro, weighted) + confusion matrix + full
                            sklearn classification report.
  * plot_confusion_matrix, plot_training_curves - saved to results/figures/
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
)

import config


# --------------------------------------------------------------------------
# Keras callback: macro recall on validation data, tracked as 'val_macro_recall'
# --------------------------------------------------------------------------
class MacroRecallCallback(tf.keras.callbacks.Callback):
    """
    Runs full validation-set inference at epoch end and injects
    'val_macro_recall' (and 'val_macro_f1') into the logs dict so that
    ModelCheckpoint/EarlyStopping can monitor it directly via
    config.MONITOR_METRIC.
    """

    def __init__(self, val_dataset: tf.data.Dataset):
        super().__init__()
        self.val_dataset = val_dataset

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        y_true, y_pred = [], []
        for images, labels in self.val_dataset:
            preds = self.model.predict(images, verbose=0)
            y_pred.extend(np.argmax(preds, axis=1))
            y_true.extend(labels.numpy())

        macro_recall = recall_score(y_true, y_pred, average="macro", zero_division=0)
        macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)

        logs["val_macro_recall"] = macro_recall
        logs["val_macro_f1"] = macro_f1
        print(f" - val_macro_recall: {macro_recall:.4f} - val_macro_f1: {macro_f1:.4f}")


# --------------------------------------------------------------------------
# Full evaluation report
# --------------------------------------------------------------------------
def compute_full_metrics(y_true, y_pred, y_proba=None) -> dict:
    """
    Parameters
    ----------
    y_true, y_pred : 1D int arrays of ground-truth / predicted class indices
    y_proba : optional (n_samples, n_classes) softmax probabilities, enables
        macro one-vs-rest ROC-AUC

    Returns
    -------
    dict with scalar summary metrics, per-class breakdown DataFrame,
    confusion matrix, and the sklearn text classification report.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    results = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "precision_weighted": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "recall_weighted": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted", zero_division=0),
    }

    per_class = pd.DataFrame({
        "class_name": [config.CLASS_LABELS[i] for i in range(config.NUM_CLASSES)],
        "precision": precision_score(y_true, y_pred, average=None, zero_division=0,
                                      labels=range(config.NUM_CLASSES)),
        "recall": recall_score(y_true, y_pred, average=None, zero_division=0,
                                labels=range(config.NUM_CLASSES)),
        "f1_score": f1_score(y_true, y_pred, average=None, zero_division=0,
                              labels=range(config.NUM_CLASSES)),
        "support": pd.Series(y_true).value_counts().reindex(range(config.NUM_CLASSES), fill_value=0).values,
    })
    results["per_class"] = per_class

    results["confusion_matrix"] = confusion_matrix(y_true, y_pred, labels=range(config.NUM_CLASSES))
    results["classification_report"] = classification_report(
        y_true, y_pred, target_names=config.CLASS_NAMES, zero_division=0
    )

    if y_proba is not None:
        try:
            results["roc_auc_macro_ovr"] = roc_auc_score(
                y_true, y_proba, average="macro", multi_class="ovr", labels=range(config.NUM_CLASSES)
            )
        except ValueError:
            results["roc_auc_macro_ovr"] = None

    return results


# --------------------------------------------------------------------------
# Plots
# --------------------------------------------------------------------------
def plot_confusion_matrix(cm: np.ndarray, save_path: str = None, normalize: bool = True, title: str = None):
    if normalize:
        cm_display = cm.astype(np.float32)
        row_sums = cm_display.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1
        cm_display = cm_display / row_sums
    else:
        cm_display = cm.astype(np.int64)

    plt.figure(figsize=(7, 6))
    sns.heatmap(cm_display, annot=True, fmt=".2f" if normalize else "d", cmap="Blues",
                xticklabels=config.CLASS_NAMES, yticklabels=config.CLASS_NAMES, cbar=True)
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.title(title or ("Normalized Confusion Matrix" if normalize else "Confusion Matrix"))
    plt.xticks(rotation=35, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=200)
    return plt.gcf()


def plot_training_curves(history: dict, save_path: str = None):
    """history: a Keras History.history dict (or merged phase1+phase2 dict)."""
    metrics_to_plot = [m for m in ["loss", "accuracy", "val_macro_recall", "val_macro_f1"] if m in history
                        or f"val_{m}" in history]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].plot(history.get("loss", []), label="train_loss")
    axes[0].plot(history.get("val_loss", []), label="val_loss")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()

    axes[1].plot(history.get("accuracy", []), label="train_accuracy")
    axes[1].plot(history.get("val_accuracy", []), label="val_accuracy")
    if "val_macro_recall" in history:
        axes[1].plot(history["val_macro_recall"], label="val_macro_recall", linestyle="--")
    if "val_macro_f1" in history:
        axes[1].plot(history["val_macro_f1"], label="val_macro_f1", linestyle="--")
    axes[1].set_title("Accuracy / Macro Recall / Macro F1")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=200)
    return fig


def save_metrics_report(results: dict, save_path: str):
    """Write a plain-text summary + classification report to disk."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        f.write("EVALUATION SUMMARY\n")
        f.write("=" * 60 + "\n")
        for key in ["accuracy", "precision_macro", "recall_macro", "f1_macro",
                    "precision_weighted", "recall_weighted", "f1_weighted", "roc_auc_macro_ovr"]:
            if key in results and results[key] is not None:
                f.write(f"{key:22s}: {results[key]:.4f}\n")
        f.write("\nPER-CLASS BREAKDOWN\n")
        f.write("-" * 60 + "\n")
        f.write(results["per_class"].to_string(index=False))
        f.write("\n\nCLASSIFICATION REPORT\n")
        f.write("-" * 60 + "\n")
        f.write(results["classification_report"])
