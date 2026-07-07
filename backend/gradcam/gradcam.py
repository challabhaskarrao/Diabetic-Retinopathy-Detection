"""
gradcam/gradcam.py
===================
Grad-CAM (Selvaraju et al., 2017) implementation for the EfficientNetB0 DR
classifier. Produces a coarse localization heatmap showing which regions of
the fundus image most influenced the model's predicted class, which is used
both for research explainability analysis (notebook) and the live Streamlit
demo.

Also includes Grad-CAM++ (Chattopadhay et al., 2018), a refinement that
tends to localize multiple / small lesions (e.g. scattered microaneurysms)
better than vanilla Grad-CAM, which matters for this task since DR lesions
are often small and numerous rather than one single salient object.
"""

import cv2
import numpy as np
import tensorflow as tf

import config


class GradCAM:
    """
    Usage:
        cam = GradCAM(model, layer_name="top_conv")
        heatmap = cam.compute_heatmap(image_batch, class_idx=predicted_class)
        overlay = cam.overlay_heatmap(original_rgb_image, heatmap)
    """

    def __init__(self, model: tf.keras.Model, layer_name: str = None):
        self.model = model
        self.layer_name = layer_name or config.GRADCAM_LAYER_NAME
        self.grad_model = self._build_grad_model()

    def _build_grad_model(self) -> tf.keras.Model:
        """
        Build a model that maps the input image to (target_conv_output,
        predictions). Works whether the target conv layer lives inside a
        nested sub-model (e.g. the EfficientNetB0 backbone wrapped as a
        layer) or directly in the top-level model.
        """
        try:
            target_layer = self.model.get_layer(self.layer_name)
            return tf.keras.Model(self.model.inputs, [target_layer.output, self.model.output])
        except ValueError:
            pass

        # Fall back to searching nested sub-models (our EfficientNet head wraps the backbone
        # as a single named layer, e.g. "efficientnetb0")
        for layer in self.model.layers:
            if hasattr(layer, "get_layer"):
                try:
                    target_layer = layer.get_layer(self.layer_name)
                    nested_grad_model = tf.keras.Model(layer.inputs, target_layer.output)

                    inputs = self.model.input
                    conv_output = nested_grad_model(inputs)
                    predictions = self.model.output
                    return tf.keras.Model(inputs, [conv_output, predictions])
                except (ValueError, AttributeError):
                    continue

        raise ValueError(
            f"Could not locate layer '{self.layer_name}' in the model or its sub-models."
        )

    def compute_heatmap(self, image_batch: np.ndarray, class_idx: int = None, eps: float = 1e-8) -> np.ndarray:
        """
        Parameters
        ----------
        image_batch : np.ndarray, shape (1, H, W, 3), already preprocessed
            exactly as for model inference (EfficientNet preprocess_input applied)
        class_idx : which class's score to explain. Defaults to the model's
            own top prediction.

        Returns
        -------
        np.ndarray heatmap, shape (H_conv, W_conv), values in [0, 1]
        """
        image_tensor = tf.convert_to_tensor(image_batch, dtype=tf.float32)

        with tf.GradientTape() as tape:
            conv_output, predictions = self.grad_model(image_tensor)
            if class_idx is None:
                class_idx = int(tf.argmax(predictions[0]))
            class_score = predictions[:, class_idx]

        grads = tape.gradient(class_score, conv_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))  # global-average-pooled gradients (alpha_k)

        conv_output = conv_output[0]
        heatmap = conv_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0)  # ReLU

        max_val = tf.reduce_max(heatmap)
        heatmap = heatmap / (max_val + eps)
        return heatmap.numpy(), class_idx

    def compute_heatmap_plusplus(self, image_batch: np.ndarray, class_idx: int = None, eps: float = 1e-8):
        """Grad-CAM++ variant: weights pixels by second-order gradient information,
        which better handles multiple/small lesion sites than vanilla Grad-CAM."""
        image_tensor = tf.convert_to_tensor(image_batch, dtype=tf.float32)

        with tf.GradientTape() as tape3:
            with tf.GradientTape() as tape2:
                with tf.GradientTape() as tape1:
                    conv_output, predictions = self.grad_model(image_tensor)
                    if class_idx is None:
                        class_idx = int(tf.argmax(predictions[0]))
                    score = predictions[:, class_idx]
                grads = tape1.gradient(score, conv_output)
            grads2 = tape2.gradient(grads, conv_output)
        grads3 = tape3.gradient(grads2, conv_output)

        global_sum = tf.reduce_sum(conv_output, axis=(1, 2), keepdims=True)
        alpha_denom = 2.0 * grads2 + global_sum * grads3
        alpha_denom = tf.where(alpha_denom != 0, alpha_denom, tf.ones_like(alpha_denom) * eps)
        alphas = grads2 / alpha_denom

        weights = tf.reduce_sum(alphas * tf.nn.relu(grads), axis=(1, 2))
        heatmap = tf.reduce_sum(weights[:, tf.newaxis, tf.newaxis, :] * conv_output, axis=-1)
        heatmap = tf.nn.relu(heatmap)[0]
        heatmap = heatmap / (tf.reduce_max(heatmap) + eps)
        return heatmap.numpy(), class_idx

    @staticmethod
    def overlay_heatmap(original_rgb: np.ndarray, heatmap: np.ndarray, alpha: float = 0.4,
                         colormap: int = cv2.COLORMAP_JET) -> np.ndarray:
        """
        Resize the low-res heatmap up to the original image size and blend
        it on top as a color overlay.

        Parameters
        ----------
        original_rgb : uint8 RGB image, any size (H, W, 3)
        heatmap : float [0,1] array from compute_heatmap()

        Returns
        -------
        uint8 RGB overlay image, same size as original_rgb
        """
        h, w = original_rgb.shape[:2]
        heatmap_resized = cv2.resize(heatmap, (w, h))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)

        heatmap_color = cv2.applyColorMap(heatmap_uint8, colormap)
        heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

        overlay = cv2.addWeighted(original_rgb.astype(np.uint8), 1 - alpha,
                                   heatmap_color, alpha, 0)
        return overlay


def generate_gradcam_explanation(model: tf.keras.Model, preprocessed_batch: np.ndarray,
                                  original_rgb_image: np.ndarray, layer_name: str = None,
                                  class_idx: int = None, use_plusplus: bool = False) -> dict:
    """
    Convenience one-shot wrapper used by inference.py and the Streamlit app.

    Returns dict with: heatmap, overlay (uint8 RGB), predicted_class_idx
    """
    cam = GradCAM(model, layer_name=layer_name)
    if use_plusplus:
        heatmap, resolved_class_idx = cam.compute_heatmap_plusplus(preprocessed_batch, class_idx)
    else:
        heatmap, resolved_class_idx = cam.compute_heatmap(preprocessed_batch, class_idx)
    overlay = cam.overlay_heatmap(original_rgb_image, heatmap)

    return {
        "heatmap": heatmap,
        "overlay": overlay,
        "predicted_class_idx": resolved_class_idx,
    }
