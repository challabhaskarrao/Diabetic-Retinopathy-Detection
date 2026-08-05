"""
streamlit_app/app.py
=====================
Streamlit demo application for the Explainable Multi-Class Diabetic
Retinopathy Detection system.

Run with:
    streamlit run streamlit_app/app.py

Features
--------
  * Fundus image upload (jpg/jpeg/png)
  * Predicted DR grade + confidence score
  * Full 5-class probability breakdown
  * Grad-CAM heatmap overlay showing which retinal regions drove the prediction
  * Plain-language disease description + suggested clinical action
  * Image-quality warning banner for blurry / poorly captured uploads
"""

import os
import sys
import time

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
from inference import load_inference_model, predict
from streamlit_app.disease_info import get_disclaimer


# --------------------------------------------------------------------------
# Page config + theme
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Diabetic Retinopathy Screening",
    page_icon=":eye:",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .main { background-color: #F7F9FB; }
    .block-container { padding-top: 2rem; }

    .app-title {
        font-size: 2.0rem;
        font-weight: 700;
        color: #0B3D62;
        margin-bottom: 0.1rem;
        letter-spacing: -0.01em;
    }
    .app-subtitle {
        color: #52657A;
        font-size: 1.0rem;
        margin-bottom: 1.4rem;
    }

    .result-card {
        background: #FFFFFF;
        border: 1px solid #E3E9EF;
        border-radius: 10px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 1px 3px rgba(11, 61, 98, 0.06);
    }
    .metric-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #7A8B9C;
        font-weight: 600;
    }
    .predicted-class {
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0.1rem 0 0.4rem 0;
    }
    .confidence-value {
        font-family: "SFMono-Regular", Consolas, monospace;
        font-size: 1.1rem;
        color: #0B3D62;
    }
    .urgency-badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: white;
    }
    .disclaimer-box {
        background: #FFF8E1;
        border: 1px solid #FFE0A3;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.85rem;
        color: #6B5300;
        margin-top: 1rem;
    }
    .quality-warning {
        background: #FDECEA;
        border: 1px solid #F5B7B1;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.86rem;
        color: #922B21;
        margin-bottom: 1rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Explainable DR Detection")
    st.caption("EfficientNetB0 + Grad-CAM · EyePACS-trained")

    model_path = st.text_input(
        "Model checkpoint path",
        value=config.EFFICIENTNET_CKPT,
        help="Path to a trained .keras model file.",
    )

    gradcam_variant = st.radio(
        "Grad-CAM variant",
        options=["Grad-CAM", "Grad-CAM++"],
        index=0,
        help="Grad-CAM++ often localizes multiple small lesions better than vanilla Grad-CAM.",
    )
    show_gradcam = st.checkbox("Show Grad-CAM explanation", value=True)

    st.markdown("---")
    st.markdown("**5-class grading scale**")
    for idx, name in config.CLASS_LABELS.items():
        info = config.DISEASE_INFO[idx]
        st.markdown(
            f"<span style='color:{info['color']}; font-weight:600;'>&#9679;</span> {idx} &mdash; {name}",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.caption(get_disclaimer())


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown('<div class="app-title">Diabetic Retinopathy Screening</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Upload a retinal fundus photograph to grade diabetic retinopathy '
    'severity (5-class) with Grad-CAM visual explanation.</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# Model loading (cached)
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading model ...")
def get_model(path):
    return load_inference_model(path)


model = None
model_load_error = None
if os.path.isfile(model_path):
    try:
        model = get_model(model_path)
    except Exception as e:  # noqa: BLE001
        model_load_error = str(e)
else:
    model_load_error = (
        f"No model checkpoint found at `{model_path}`. Train a model first with "
        f"`python train.py`, or point this field at an existing `.keras` file."
    )

if model_load_error:
    st.warning(model_load_error)


# --------------------------------------------------------------------------
# Upload + inference
# --------------------------------------------------------------------------
uploaded_file = st.file_uploader("Upload a fundus image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and model is not None:
    pil_image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(pil_image)

    with st.spinner("Analyzing image ..."):
        t0 = time.time()
        result = predict(
            image_array,
            model=model,
            run_gradcam=show_gradcam,
            use_gradcam_plusplus=(gradcam_variant == "Grad-CAM++"),
        )
        elapsed_ms = (time.time() - t0) * 1000

    if not result["quality"]["is_usable"]:
        st.markdown(
            f'<div class="quality-warning">&#9888; Image quality flag: '
            f'<b>{result["quality"]["reason"]}</b>. Prediction may be less reliable - '
            f"consider re-capturing this image.</div>",
            unsafe_allow_html=True,
        )

    col_image, col_gradcam = st.columns(2)
    with col_image:
        st.markdown("**Uploaded image**")
        st.image(pil_image, use_container_width=True)
    with col_gradcam:
        if show_gradcam and result["gradcam_overlay"] is not None:
            st.markdown(f"**{gradcam_variant} explanation**")
            st.image(result["gradcam_overlay"], use_container_width=True)
        else:
            st.markdown("**Grad-CAM explanation**")
            st.info("Enable 'Show Grad-CAM explanation' in the sidebar to visualize model attention.")

    st.markdown("<br>", unsafe_allow_html=True)

    info = result["disease_info"]
    col_result, col_probs = st.columns([1, 1.3])

    with col_result:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Predicted grade</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="predicted-class" style="color:{info["color"]};">{info["label"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-label">Confidence</div>'
            f'<div class="confidence-value">{result["confidence"] * 100:.1f}%</div>',
            unsafe_allow_html=True,
        )
        st.progress(min(max(result["confidence"], 0.0), 1.0))

        st.markdown(
            f'<br><span class="urgency-badge" style="background:{info["color"]};">'
            f'{info["urgency"]}</span>',
            unsafe_allow_html=True,
        )

        st.markdown(f"<p style='margin-top:1rem;'>{info['detail']}</p>", unsafe_allow_html=True)
        st.caption(f"Inference time: {elapsed_ms:.0f} ms")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_probs:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Class probability breakdown</div>', unsafe_allow_html=True)
        prob_df = pd.DataFrame({
            "Class": list(result["class_probabilities"].keys()),
            "Probability": list(result["class_probabilities"].values()),
        }).set_index("Class")
        st.bar_chart(prob_df, height=280)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f'<div class="disclaimer-box">{get_disclaimer()}</div>',
        unsafe_allow_html=True,
    )

    with st.expander("Raw prediction JSON"):
        st.json({k: v for k, v in result.items() if k not in ("gradcam_overlay", "gradcam_heatmap")})

elif uploaded_file is not None and model is None:
    st.error("Cannot run inference: no model is loaded. See the warning above.")
else:
    st.info("Upload a retinal fundus image (JPG/PNG) above to get started.")
