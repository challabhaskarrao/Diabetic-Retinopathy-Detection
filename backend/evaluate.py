"""
evaluate.py
===========
Standalone evaluation of a trained model on the held-out test set.
Produces:
  * accuracy, precision, recall, F1 (macro + weighted + per-class)
  * confusion matrix (raw + normalized, saved as PNG)
  * full sklearn classification report (saved as .txt)
  * per-class metrics table (saved as .csv)

Usage
-----
    python evaluate.py --model results_path/efficientnet_b0_best.keras
    python evaluate.py --model models/saved_models/efficientnet_b0_best.keras --split test
"""

import argparse
import os

import numpy as np
import tensorflow as tf

import config
from utils.data_loader import build_dataset, get_labels_array
from utils.metrics import compute_full_metrics, plot_confusion_matrix, save_metrics_report


def run_evaluation(model_path: str, csv_path: str, tag: str = "test"):
    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(model_path, compile=False)

    ds = build_dataset(csv_path, training=False)
    y_true = get_labels_array(csv_path)

    print("Running inference on the evaluation set ...")
    y_proba = model.predict(ds, verbose=1)
    y_pred = np.argmax(y_proba, axis=1)

    results = compute_full_metrics(y_true, y_pred, y_proba)

    print("\n" + "=" * 60)
    print(f"RESULTS ({tag})")
    print("=" * 60)
    for key in ["accuracy", "precision_macro", "recall_macro", "f1_macro", "roc_auc_macro_ovr"]:
        val = results.get(key)
        if val is not None:
            print(f"{key:22s}: {val:.4f}")
    print("\nPer-class breakdown:")
    print(results["per_class"].to_string(index=False))
    print("\n" + results["classification_report"])

    # persist artifacts
    plot_confusion_matrix(
        results["confusion_matrix"],
        save_path=os.path.join(config.FIGURES_DIR, f"confusion_matrix_{tag}.png"),
        normalize=True,
        title=f"Confusion Matrix - {tag} set (normalized)",
    )
    plot_confusion_matrix(
        results["confusion_matrix"],
        save_path=os.path.join(config.FIGURES_DIR, f"confusion_matrix_{tag}_counts.png"),
        normalize=False,
        title=f"Confusion Matrix - {tag} set (counts)",
    )
    save_metrics_report(results, os.path.join(config.REPORTS_DIR, f"metrics_report_{tag}.txt"))
    results["per_class"].to_csv(os.path.join(config.REPORTS_DIR, f"per_class_metrics_{tag}.csv"), index=False)

    print(f"\nSaved confusion matrix + report to: {config.FIGURES_DIR} / {config.REPORTS_DIR}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a trained DR classifier.")
    parser.add_argument("--model", type=str, default=config.EFFICIENTNET_CKPT,
                         help="Path to a saved .keras model.")
    parser.add_argument("--split", type=str, default="test", choices=["val", "test"],
                         help="Which manifest split to evaluate on.")
    args = parser.parse_args()

    csv_path = config.TEST_CSV if args.split == "test" else config.VAL_CSV
    run_evaluation(args.model, csv_path, tag=args.split)
