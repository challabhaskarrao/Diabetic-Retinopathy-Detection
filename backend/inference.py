"""
inference.py
=============
Single-image inference pipeline: preprocessing -> prediction -> confidence
scores -> Grad-CAM explanation -> disease description.

This is the module both the CLI (`python inference.py --image path.jpg`)
and the Streamlit app (streamlit_app/app.py) call into, so behaviour is
guaranteed to be identical between local testing and the deployed demo.
"""

import argparse
import functools

import numpy as np
import tensorflow as tf

import config
from gradcam.gradcam import generate_gradcam_explanation
from utils.preprocessing import assess_image_quality, load_image, preprocess_image


@functools.lru_cache(maxsize=1)
def load_inference_model(model_path: str = None) -> tf.keras.Model:
    """Cached model load so Streamlit doesn't reload weights on every rerun."""
    model_path = model_path or config.EFFICIENTNET_CKPT
    return tf.keras.models.load_model(model_path, compile=False)


def predict(image_path_or_array, model: tf.keras.Model = None, model_path: str = None,
            run_gradcam: bool = True, use_gradcam_plusplus: bool = False) -> dict:
    """
    Full inference pipeline for a single fundus image.

    Parameters
    ----------
    image_path_or_array : str path OR an already-loaded RGB uint8 np.ndarray
    model : optionally pass an already-loaded model to skip disk I/O
    run_gradcam : whether to compute the Grad-CAM overlay (slightly slower)

    Returns
    -------
    dict with keys:
        predicted_class_idx, predicted_class_name, confidence,
        class_probabilities (dict class_name -> prob), quality (dict),
        disease_info (dict), gradcam_overlay (uint8 RGB array or None)
    """
    model = model or load_inference_model(model_path)

    original_rgb = load_image(image_path_or_array) if isinstance(image_path_or_array, str) \
        else image_path_or_array

    quality = assess_image_quality(original_rgb)

    preprocessed = preprocess_image(original_rgb)                 # float32 [0,1], 224x224x3
    model_input = (preprocessed * 255.0).astype(np.float32)
    model_input = tf.keras.applications.efficientnet.preprocess_input(model_input)
    batch = np.expand_dims(model_input, axis=0)

    probabilities = model.predict(batch, verbose=0)[0]
    predicted_idx = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_idx])

    result = {
        "predicted_class_idx": predicted_idx,
        "predicted_class_name": config.CLASS_LABELS[predicted_idx],
        "confidence": confidence,
        "class_probabilities": {
            config.CLASS_LABELS[i]: float(probabilities[i]) for i in range(config.NUM_CLASSES)
        },
        "quality": quality,
        "disease_info": config.DISEASE_INFO[predicted_idx],
        "gradcam_overlay": None,
        "gradcam_heatmap": None,
    }

    if run_gradcam:
        # Resize the *original* image to a consistent display size so the overlay looks clean
        import cv2
        display_size = 512
        display_original = cv2.resize(original_rgb, (display_size, display_size))
        # re-run preprocessing at the display resolution isn't necessary; instead map
        # the model-resolution heatmap back onto the display-resolution original image.
        gradcam_result = generate_gradcam_explanation(
            model, batch, display_original, class_idx=predicted_idx,
            use_plusplus=use_gradcam_plusplus,
        )
        result["gradcam_overlay"] = gradcam_result["overlay"]
        result["gradcam_heatmap"] = gradcam_result["heatmap"]

    return result


def format_result_text(result: dict) -> str:
    lines = [
        f"Prediction: {result['predicted_class_name']} (class {result['predicted_class_idx']})",
        f"Confidence: {result['confidence'] * 100:.2f}%",
        "",
        "Class probabilities:",
    ]
    for name, prob in result["class_probabilities"].items():
        lines.append(f"  {name:20s}: {prob * 100:6.2f}%")
    lines += [
        "",
        f"Image quality: {'OK' if result['quality']['is_usable'] else 'FLAGGED - ' + result['quality']['reason']}",
        "",
        f"Clinical note: {result['disease_info']['summary']}",
        f"{result['disease_info']['detail']}",
        f"Suggested action: {result['disease_info']['urgency']}",
        "",
        config.DISCLAIMER,
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference on a single fundus image.")
    parser.add_argument("--image", type=str, required=True, help="Path to a fundus image.")
    parser.add_argument("--model", type=str, default=None, help="Path to a saved .keras model.")
    parser.add_argument("--no-gradcam", action="store_true", help="Skip Grad-CAM computation.")
    args = parser.parse_args()

    result = predict(args.image, model_path=args.model, run_gradcam=not args.no_gradcam)
    print(format_result_text(result))

    if result["gradcam_overlay"] is not None:
        import cv2
        out_path = "gradcam_output.png"
        cv2.imwrite(out_path, cv2.cvtColor(result["gradcam_overlay"], cv2.COLOR_RGB2BGR))
        print(f"\nGrad-CAM overlay saved to: {out_path}")
