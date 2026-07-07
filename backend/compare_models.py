"""
compare_models.py
==================
Research-enhancement script: evaluates the from-scratch baseline CNN and
the transfer-learned EfficientNetB0 model on the identical held-out test
set, then produces a side-by-side comparison table, a grouped bar chart,
and a written "performance improvement analysis" summarizing the effect of
transfer learning + fine-tuning for this task.

Usage
-----
    python compare_models.py
    python compare_models.py --baseline models/saved_models/baseline_cnn_best.keras \
                              --efficientnet models/saved_models/efficientnet_b0_best.keras
"""

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

import config
from utils.data_loader import build_dataset, get_labels_array
from utils.metrics import compute_full_metrics


def evaluate_model(model_path: str, csv_path: str) -> dict:
    model = tf.keras.models.load_model(model_path, compile=False)
    ds = build_dataset(csv_path, training=False)
    y_true = get_labels_array(csv_path)
    y_proba = model.predict(ds, verbose=0)
    y_pred = np.argmax(y_proba, axis=1)
    n_params = model.count_params()
    return {**compute_full_metrics(y_true, y_pred, y_proba), "n_params": n_params}


def build_comparison_table(baseline_results: dict, efficientnet_results: dict) -> pd.DataFrame:
    rows = []
    metric_keys = [
        ("accuracy", "Accuracy"),
        ("precision_macro", "Precision (macro)"),
        ("recall_macro", "Recall (macro)"),
        ("f1_macro", "F1-score (macro)"),
        ("roc_auc_macro_ovr", "ROC-AUC (macro, OvR)"),
    ]
    for key, label in metric_keys:
        base_val = baseline_results.get(key)
        eff_val = efficientnet_results.get(key)
        if base_val is None or eff_val is None:
            continue
        abs_improvement = eff_val - base_val
        rel_improvement = (abs_improvement / base_val * 100) if base_val > 0 else float("nan")
        rows.append({
            "Metric": label,
            "Baseline CNN": round(base_val, 4),
            "EfficientNetB0": round(eff_val, 4),
            "Absolute Improvement": round(abs_improvement, 4),
            "Relative Improvement (%)": round(rel_improvement, 2),
        })

    rows.append({
        "Metric": "Trainable/Total Parameters",
        "Baseline CNN": baseline_results["n_params"],
        "EfficientNetB0": efficientnet_results["n_params"],
        "Absolute Improvement": efficientnet_results["n_params"] - baseline_results["n_params"],
        "Relative Improvement (%)": float("nan"),
    })

    return pd.DataFrame(rows)


def plot_comparison_bar(comparison_df: pd.DataFrame, save_path: str):
    plot_df = comparison_df[comparison_df["Metric"] != "Trainable/Total Parameters"]

    x = np.arange(len(plot_df))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width / 2, plot_df["Baseline CNN"], width, label="Baseline CNN", color="#9E9E9E")
    ax.bar(x + width / 2, plot_df["EfficientNetB0"], width, label="EfficientNetB0 (Transfer Learning)",
           color="#1565C0")

    ax.set_ylabel("Score")
    ax.set_title("Baseline CNN vs. EfficientNetB0: Test-Set Performance")
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df["Metric"], rotation=25, ha="right")
    ax.set_ylim(0, 1.0)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=200)
    return fig


def write_improvement_analysis(comparison_df: pd.DataFrame, save_path: str):
    f1_row = comparison_df[comparison_df["Metric"] == "F1-score (macro)"].iloc[0]
    recall_row = comparison_df[comparison_df["Metric"] == "Recall (macro)"].iloc[0]
    param_row = comparison_df[comparison_df["Metric"] == "Trainable/Total Parameters"].iloc[0]

    text = f"""PERFORMANCE IMPROVEMENT ANALYSIS
{"=" * 60}
Baseline: a 4-block CNN trained from scratch (random initialization).
Comparison model: EfficientNetB0 pretrained on ImageNet, fine-tuned in
two phases (frozen-backbone head training, then partial backbone
fine-tuning) on the EyePACS training split.

Macro F1-score improved by {f1_row['Absolute Improvement']:.4f} absolute
({f1_row['Relative Improvement (%)']:.1f}% relative) when moving from the
baseline CNN to EfficientNetB0 with transfer learning.

Macro recall - the metric this project explicitly optimizes for, since
missing a true DR case is the costliest error in a screening context -
improved by {recall_row['Absolute Improvement']:.4f} absolute
({recall_row['Relative Improvement (%)']:.1f}% relative).

Parameter count changed by {param_row['Absolute Improvement']:,} (baseline:
{param_row['Baseline CNN']:,}, EfficientNetB0: {param_row['EfficientNetB0']:,}),
which should be read alongside accuracy: the goal of choosing EfficientNetB0
over larger backbones (ResNet50/InceptionV3/DenseNet121) was to obtain most
of the transfer-learning benefit at a fraction of the inference cost.

Interpretation
--------------
1. Transfer learning from ImageNet gives the model useful low/mid-level
   visual filters (edges, blob detectors, color-contrast detectors) "for
   free", which is especially valuable here because labelled fundus images
   are far scarcer than labelled natural images, and DR lesions
   (microaneurysms, haemorrhages, exudates) share low-level visual
   structure with the blob/edge patterns ImageNet features already encode.
2. Two-phase fine-tuning (frozen head training, then careful partial
   backbone unfreezing at a low learning rate) avoids catastrophic
   forgetting while still letting late-stage backbone filters specialize
   to fundus-image statistics (color balance, vessel texture) that differ
   from natural images.
3. The from-scratch baseline, lacking any prior visual knowledge, must
   learn all of this from a comparatively small, imbalanced dataset, which
   typically shows up as weaker performance specifically on the rarer
   classes (Severe / Proliferative DR) - see per-class recall in the full
   evaluation report for a class-by-class breakdown.

Note: the exact figures above are computed from your actual training run;
re-run `python compare_models.py` after training both models on the full
EyePACS dataset to regenerate this report with final numbers.
"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        f.write(text)
    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare baseline CNN vs EfficientNetB0.")
    parser.add_argument("--baseline", type=str, default=config.BASELINE_CKPT)
    parser.add_argument("--efficientnet", type=str, default=config.EFFICIENTNET_CKPT)
    parser.add_argument("--split", type=str, default="test", choices=["val", "test"])
    args = parser.parse_args()

    csv_path = config.TEST_CSV if args.split == "test" else config.VAL_CSV

    print("Evaluating baseline CNN ...")
    baseline_results = evaluate_model(args.baseline, csv_path)

    print("Evaluating EfficientNetB0 ...")
    efficientnet_results = evaluate_model(args.efficientnet, csv_path)

    comparison_df = build_comparison_table(baseline_results, efficientnet_results)
    print("\n" + comparison_df.to_string(index=False))

    comparison_df.to_csv(os.path.join(config.REPORTS_DIR, "model_comparison.csv"), index=False)
    plot_comparison_bar(comparison_df, os.path.join(config.FIGURES_DIR, "model_comparison_bar.png"))
    analysis_text = write_improvement_analysis(
        comparison_df, os.path.join(config.REPORTS_DIR, "performance_improvement_analysis.txt")
    )
    print("\n" + analysis_text)
