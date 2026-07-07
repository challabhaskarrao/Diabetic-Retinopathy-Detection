"""
streamlit_app/disease_info.py
==============================
Thin wrapper around config.DISEASE_INFO for the Streamlit app, kept as a
separate module so app.py stays focused on layout/interaction and the
clinical copy can be edited/reviewed independently (e.g. by a medical
reviewer) without touching app logic.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config


def get_disease_info(class_idx: int) -> dict:
    return config.DISEASE_INFO[class_idx]


def get_all_disease_info() -> dict:
    return config.DISEASE_INFO


def get_disclaimer() -> str:
    return config.DISCLAIMER
