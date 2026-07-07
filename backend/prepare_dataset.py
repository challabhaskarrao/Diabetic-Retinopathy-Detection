"""
prepare_dataset.py
===================
One-time dataset preparation script for the EyePACS Diabetic Retinopathy
dataset from Kaggle.

This does NOT download the dataset automatically inside this repo (EyePACS
is ~35-90GB depending on which Kaggle mirror you use and requires you to
accept its competition rules on Kaggle first). Instead:

  1. You download it yourself (see dataset/README.md for the exact Kaggle
     CLI commands).
  2. Point --source-csv / --image-dir at wherever you extracted it.
  3. This script builds stratified train/val/test manifests
     (dataset/train_labels.csv, val_labels.csv, test_labels.csv) with an
     absolute `filepath` column that every other module reads from.

Usage
-----
    python prepare_dataset.py \\
        --source-csv /path/to/trainLabels.csv \\
        --image-dir /path/to/train_images \\
        --extension .jpeg
"""

import argparse

import config
from utils.class_imbalance import class_distribution_report
from utils.data_loader import create_splits


def main():
    parser = argparse.ArgumentParser(description="Prepare stratified EyePACS train/val/test manifests.")
    parser.add_argument("--source-csv", type=str, required=True,
                         help="Path to the raw EyePACS labels CSV (image, level columns).")
    parser.add_argument("--image-dir", type=str, default=config.RAW_IMAGE_DIR,
                         help="Directory containing the raw fundus image files.")
    parser.add_argument("--extension", type=str, default=config.IMAGE_EXTENSION)
    parser.add_argument("--image-col", type=str, default="image")
    parser.add_argument("--label-col", type=str, default="level")
    args = parser.parse_args()

    print("Building stratified train/val/test splits ...")
    train_df, val_df, test_df = create_splits(
        source_csv=args.source_csv,
        image_col=args.image_col,
        label_col=args.label_col,
        image_dir=args.image_dir,
        extension=args.extension,
    )

    print(f"\nTrain: {len(train_df)} images  ->  {config.TRAIN_CSV}")
    print(f"Val:   {len(val_df)} images  ->  {config.VAL_CSV}")
    print(f"Test:  {len(test_df)} images  ->  {config.TEST_CSV}")

    print("\nTrain split class distribution:")
    print(class_distribution_report(train_df["level"].values).to_string(index=False))
    print("\nVal split class distribution:")
    print(class_distribution_report(val_df["level"].values).to_string(index=False))
    print("\nTest split class distribution:")
    print(class_distribution_report(test_df["level"].values).to_string(index=False))

    print("\nDone. Next step: python train.py")


if __name__ == "__main__":
    main()
