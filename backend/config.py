"""
config.py
=========
Central configuration for the Explainable Multi-Class Diabetic Retinopathy
Detection project. Every other module imports its constants from here so
that paths, hyperparameters, and class definitions stay consistent across
preprocessing, training, evaluation, Grad-CAM, and the Streamlit app.

Edit this file to point at your local copy of the EyePACS dataset and to
tune experiment hyperparameters. Nothing here requires code changes
elsewhere in the project.
"""

import os

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")
RAW_IMAGE_DIR = os.path.join(DATASET_DIR, "raw_images")          # original EyePACS .jpeg files
PROCESSED_IMAGE_DIR = os.path.join(DATASET_DIR, "processed_images")  # resized/cleaned copies (optional cache)
TRAIN_CSV = os.path.join(DATASET_DIR, "train_labels.csv")        # columns: image, level
VAL_CSV = os.path.join(DATASET_DIR, "val_labels.csv")
TEST_CSV = os.path.join(DATASET_DIR, "test_labels.csv")

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
SAVED_MODELS_DIR = os.path.join(MODELS_DIR, "saved_models")
BASELINE_CKPT = os.path.join(SAVED_MODELS_DIR, "baseline_cnn_best.keras")
EFFICIENTNET_CKPT = os.path.join(SAVED_MODELS_DIR, "efficientnet_b0_best.keras")
EFFICIENTNET_FINAL = os.path.join(SAVED_MODELS_DIR, "efficientnet_b0_final.keras")
TFLITE_MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "efficientnet_b0_lite.tflite")

RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
LOGS_DIR = os.path.join(RESULTS_DIR, "logs")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")
GRADCAM_OUTPUT_DIR = os.path.join(RESULTS_DIR, "gradcam_samples")
REPORTS_DIR = os.path.join(RESULTS_DIR, "reports")

for _d in [DATASET_DIR, RAW_IMAGE_DIR, PROCESSED_IMAGE_DIR, SAVED_MODELS_DIR,
           LOGS_DIR, FIGURES_DIR, GRADCAM_OUTPUT_DIR, REPORTS_DIR]:
    os.makedirs(_d, exist_ok=True)

# --------------------------------------------------------------------------
# Class definitions (EyePACS / APTOS DR grading scale)
# --------------------------------------------------------------------------
NUM_CLASSES = 5
CLASS_NAMES = ["No_DR", "Mild", "Moderate", "Severe", "Proliferative_DR"]
CLASS_LABELS = {
    0: "No DR",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Proliferative DR",
}

# --------------------------------------------------------------------------
# Image / preprocessing settings
# --------------------------------------------------------------------------
IMG_SIZE = 224                     # EfficientNetB0 native input resolution
IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)
IMAGE_EXTENSION = ".jpeg"          # EyePACS raw files ship as .jpeg

APPLY_BEN_GRAHAM_PREPROCESSING = True   # local-average subtraction (Kaggle-winning technique)
APPLY_DENOISING = True                  # mild denoising for low-quality fundus captures
BLUR_VARIANCE_THRESHOLD = 15.0          # Laplacian-variance floor for "usable" images
DARK_PIXEL_FRACTION_THRESHOLD = 0.55    # flags images that are mostly black (bad crop / capture)

# --------------------------------------------------------------------------
# Augmentation settings
# --------------------------------------------------------------------------
ROTATION_RANGE = 0.10        # fraction of 2*pi radians (~36 degrees) passed to RandomRotation
ZOOM_RANGE = 0.15
BRIGHTNESS_RANGE = 0.20
CONTRAST_RANGE = 0.15
HORIZONTAL_FLIP = True

# --------------------------------------------------------------------------
# Data split / loading
# --------------------------------------------------------------------------
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_SEED = 42
BATCH_SIZE = 32
SHUFFLE_BUFFER = 2048

# --------------------------------------------------------------------------
# Class imbalance handling
# --------------------------------------------------------------------------
USE_CLASS_WEIGHTS = True
USE_OVERSAMPLING = False     # set True to additionally rebalance via tf.data resampling
OVERSAMPLE_TARGET_DIST = None  # None => uniform target distribution across classes

# --------------------------------------------------------------------------
# Model / training hyperparameters
# --------------------------------------------------------------------------
BACKBONE = "EfficientNetB0"
DROPOUT_RATE = 0.4
DENSE_UNITS = 256
L2_REG = 1e-4

# Phase 1: train classification head only, backbone frozen
PHASE1_EPOCHS = 15
PHASE1_LR = 1e-3

# Phase 2: fine-tune top N layers of the backbone at a low learning rate
PHASE2_EPOCHS = 20
PHASE2_LR = 1e-5
FINE_TUNE_AT_LAYER = 100     # unfreeze layers from this index onward (EfficientNetB0 has ~237 layers)

EARLY_STOPPING_PATIENCE = 6
REDUCE_LR_PATIENCE = 3
REDUCE_LR_FACTOR = 0.5
MIN_LR = 1e-7

# Monitor macro recall (not just accuracy) so checkpointing/early-stopping favor the
# metric that matters most for medical screening safety: catching every DR case.
MONITOR_METRIC = "val_macro_recall"
MONITOR_MODE = "max"

GRADCAM_LAYER_NAME = "top_conv"   # EfficientNetB0's final feature map before pooling

# --------------------------------------------------------------------------
# Disease descriptions (used by inference.py and the Streamlit app)
# --------------------------------------------------------------------------
DISEASE_INFO = {
    0: {
        "label": "No DR",
        "summary": "No visible signs of diabetic retinopathy.",
        "detail": (
            "The retina shows no microaneurysms, haemorrhages, or exudates. "
            "Continue routine annual diabetic eye screening as recommended by a physician."
        ),
        "urgency": "Routine",
        "color": "#2E7D32",
    },
    1: {
        "label": "Mild",
        "summary": "Mild non-proliferative diabetic retinopathy (NPDR).",
        "detail": (
            "Early-stage changes limited to a small number of microaneurysms. "
            "Typically requires monitoring and tighter glycemic control rather than immediate treatment."
        ),
        "urgency": "Monitor / re-screen in 12 months",
        "color": "#9E9D24",
    },
    2: {
        "label": "Moderate",
        "summary": "Moderate non-proliferative diabetic retinopathy.",
        "detail": (
            "More extensive microaneurysms, haemorrhages, and/or venous beading are present. "
            "Referral to an ophthalmologist for closer monitoring is generally advised."
        ),
        "urgency": "Referral recommended within 3-6 months",
        "color": "#EF6C00",
    },
    3: {
        "label": "Severe",
        "summary": "Severe non-proliferative diabetic retinopathy.",
        "detail": (
            "Widespread haemorrhages, venous beading in multiple quadrants, and/or intraretinal "
            "microvascular abnormalities. High risk of progressing to proliferative disease."
        ),
        "urgency": "Prompt ophthalmology referral (within weeks)",
        "color": "#D84315",
    },
    4: {
        "label": "Proliferative DR",
        "summary": "Proliferative diabetic retinopathy (PDR).",
        "detail": (
            "Neovascularisation and/or vitreous/pre-retinal haemorrhage are present. "
            "This is a sight-threatening stage requiring urgent specialist care."
        ),
        "urgency": "Urgent ophthalmology referral",
        "color": "#B71C1C",
    },
}

DISCLAIMER = (
    "This tool is a research / decision-support prototype. It is NOT a certified "
    "medical device and must not be used as the sole basis for diagnosis or treatment. "
    "Always confirm findings with a qualified ophthalmologist."
)
