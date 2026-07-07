"""
optimize_model.py
==================
Converts the trained Keras EfficientNetB0 model to TensorFlow Lite for
lightweight inference (edge devices, low-resource clinic hardware, or
simply faster/cheaper server-side serving). Supports optional post-training
dynamic-range or float16 quantization.

Usage
-----
    python optimize_model.py                              # dynamic-range quantization (default)
    python optimize_model.py --quantization float16
    python optimize_model.py --quantization none           # plain float32 TFLite, no quantization

Note: full integer quantization (int8) is intentionally not the default for
this medical-screening use case, since it requires a representative
calibration dataset and can shift decision boundaries; validate any
quantized model's per-class recall against the float baseline before
deploying it (see evaluate.py) rather than assuming size reduction is free.
"""

import argparse
import os

import tensorflow as tf

import config


def convert_to_tflite(model_path: str, output_path: str, quantization: str = "dynamic"):
    model = tf.keras.models.load_model(model_path, compile=False)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    if quantization == "dynamic":
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
    elif quantization == "float16":
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.float16]
    elif quantization == "none":
        pass
    else:
        raise ValueError(f"Unknown quantization mode: {quantization}")

    tflite_model = converter.convert()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(tflite_model)

    original_size_mb = os.path.getsize(model_path) / (1024 ** 2) if os.path.isfile(model_path) else None
    tflite_size_mb = len(tflite_model) / (1024 ** 2)

    print(f"TFLite model saved to: {output_path}")
    print(f"TFLite model size: {tflite_size_mb:.2f} MB")
    if original_size_mb:
        print(f"Original Keras model size: {original_size_mb:.2f} MB "
              f"({(1 - tflite_size_mb / original_size_mb) * 100:.1f}% smaller)")

    return output_path


def benchmark_tflite(tflite_path: str, n_runs: int = 50):
    """Rough single-image latency benchmark for the converted model."""
    import time
    import numpy as np

    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    dummy_input = np.random.rand(*input_details[0]["shape"]).astype(input_details[0]["dtype"])

    # warm-up
    for _ in range(5):
        interpreter.set_tensor(input_details[0]["index"], dummy_input)
        interpreter.invoke()

    start = time.time()
    for _ in range(n_runs):
        interpreter.set_tensor(input_details[0]["index"], dummy_input)
        interpreter.invoke()
        _ = interpreter.get_tensor(output_details[0]["index"])
    elapsed = time.time() - start

    avg_ms = (elapsed / n_runs) * 1000
    print(f"Average single-image inference latency: {avg_ms:.2f} ms over {n_runs} runs")
    return avg_ms


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert the trained model to TFLite for lightweight inference.")
    parser.add_argument("--model", type=str, default=config.EFFICIENTNET_CKPT)
    parser.add_argument("--output", type=str, default=config.TFLITE_MODEL_PATH)
    parser.add_argument("--quantization", type=str, default="dynamic",
                         choices=["dynamic", "float16", "none"])
    parser.add_argument("--benchmark", action="store_true")
    args = parser.parse_args()

    out_path = convert_to_tflite(args.model, args.output, args.quantization)
    if args.benchmark:
        benchmark_tflite(out_path)
