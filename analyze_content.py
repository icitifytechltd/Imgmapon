"""
analyze_content.py
------------------
Image analysis helpers for IMG MAPON

Features:
 - dominant_colors(image: PIL.Image or path) -> list hex colors
 - detect_edges(image) -> edge density float
 - detect_objects(image_path, model_dir) -> list of detected objects (MobileNet-SSD)
 - detect_faces(image) -> face bboxes via OpenCV Haar cascade
 - ocr_text(image) -> extracted text (pytesseract)
 - reverse_geocode(lat, lon) -> dict with address (geopy)
 - generate_html_report(output_dir, results_dict) -> writes a simple HTML with thumbnails and JSON
 - download_mobilenet_ssd(model_dir) -> helper to fetch model files
"""

from __future__ import annotations
import os
import io
import json
import math
import shutil
import tempfile
from typing import List, Dict, Tuple, Optional

from PIL import Image, ImageOps

# Optional imports
try:
    import cv2
except Exception:
    cv2 = None

try:
    import numpy as np
except Exception:
    np = None

try:
    from sklearn.cluster import KMeans
except Exception:
    KMeans = None

try:
    import pytesseract
except Exception:
    pytesseract = None

try:
    from geopy.geocoders import Nominatim
except Exception:
    Nominatim = None

import requests

# MobileNet-SSD model filenames (Caffe)
MSSD_PROTO = "deploy.prototxt"
# this is face-ssd name; below we use object SSD if provided
MSSD_MODEL = "res10_300x300_ssd_iter_140000.caffemodel"
# We'll use MobileNet-SSD (object) names below; user can supply model_dir with prototxt & caffemodel


def _open_image(input_image) -> Image.Image:
    if isinstance(input_image, Image.Image):
        return input_image
    if isinstance(input_image, (str, bytes)):
        if isinstance(input_image, str) and input_image.lower().startswith(("http://", "https://")):
            r = requests.get(input_image, timeout=15)
            r.raise_for_status()
            return Image.open(io.BytesIO(r.content)).convert("RGB")
        return Image.open(input_image).convert("RGB")
    raise ValueError("Unsupported image input")


def dominant_colors(input_image, k: int = 6) -> Dict[str, object]:
    """
    Return dominant colors as hex list and rgb list.
    Accepts PIL.Image or path/url.
    """
    img = _open_image(input_image)
    # resize to speed up
    small = img.copy()
    small.thumbnail((300, 300))
    arr = np.array(small).reshape(-1,
                   3).astype(float) if np is not None else None

    if arr is None:
        return {"error": "numpy required for dominant_colors"}

    # If sklearn KMeans available use it
    if KMeans is not None:
        km = KMeans(n_clusters=min(k, 8), random_state=0, n_init=4)
        km.fit(arr)
        centers = km.cluster_centers_.astype(int)
    else:
        # Simple iterative kmeans fallback
        # initialize centers from evenly spaced pixels
        idxs = np.linspace(0, arr.shape[0] - 1, min(k, 8)).astype(int)
        centers = arr[idxs].copy()
        for _ in range(6):
            dists = np.linalg.norm(
                arr[:, None, :] - centers[None, :, :], axis=2)
            labels = dists.argmin(axis=1)
            new_centers = []
            for i in range(centers.shape[0]):
                pts = arr[labels == i]
                if len(pts) == 0:
                    new_centers.append(centers[i])
                else:
                    new_centers.append(pts.mean(axis=0))
            centers = np.vstack(new_centers)
        centers = centers.astype(int)

    hex_colors = ["#%02x%02x%02x" % tuple(c) for c in centers]
    return {"hex": hex_colors, "rgb": centers.tolist()}


def detect_edges(input_image) -> Dict[str, object]:
    """
    Returns an edge density metric (0..1).
    """
    img = _open_image(input_image)
    if cv2 is None or np is None:
        return {"error": "opencv-python and numpy are required for edge detection"}
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_ratio = float((edges > 0).sum()) / edges.size
    return {"edge_ratio": round(edge_ratio, 4)}


def detect_faces(input_image, save_annotated: Optional[str] = None) -> Dict[str, object]:
    """
    Uses OpenCV Haar cascade to detect faces.
    Optionally writes annotated image to save_annotated.
    """
    img = _open_image(input_image)
    if cv2 is None or np is None:
        return {"error": "opencv-python and numpy required for face detection"}

    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    if not os.path.exists(cascade_path):
        return {"error": "haarcascade not found in OpenCV installation"}

    face_cascade = cv2.CascadeClassifier(cascade_path)
    arr = np.array(img.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
    boxes = [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)}
                       for (x, y, w, h) in faces.tolist()]

    if save_annotated and boxes:
        draw = img.copy()
        from PIL import ImageDraw
        d = ImageDraw.Draw(draw)
        for b in boxes:
            d.rectangle([b["x"], b["y"], b["x"] + b["w"],
                        b["y"] + b["h"]], outline=(255, 0, 0), width=3)
        draw.save(save_annotated)

    return {"count": len(boxes), "faces": boxes}


def ocr_text(input_image) -> Dict[str, object]:
    """
    Extract text using pytesseract. Returns full text and a short snippet.
    Requires Tesseract installed (system) and pytesseract Python package.
    """
    img = _open_image(input_image)
    if pytesseract is None:
        return {"error": "pytesseract not installed"}
    try:
        text = pytesseract.image_to_string(img)
        return {"text": text, "snippet": text.strip()[:1000], "len": len(text)}
    except Exception as e:
        return {"error": str(e)}


def download_mobilenet_ssd(target_dir: str) -> Dict[str, object]:
    """
    Helper to download MobileNet-SSD object detection model files (Caffe).
    Writes deploy.prototxt and caffemodel into target_dir.
    NOTE: Files are ~20-100MB depending on model; user must accept bandwidth.
    """
    os.makedirs(target_dir, exist_ok=True)
    # Common lightweight SSD MobileNet v1 Caffe model from OpenCV's GitHub or other mirrors
    proto_url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/deploy.prototxt"
    model_url = "https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.caffemodel"
    proto_path = os.path.join(target_dir, "MobileNetSSD_deploy.prototxt")
    model_path = os.path.join(target_dir, "MobileNetSSD_deploy.caffemodel")
    stats = {}
    for url, path in [(proto_url, proto_path), (model_url, model_path)]:
        if os.path.exists(path):
            stats[path] = "exists"
            continue
        try:
            r = requests.get(url, stream=True, timeout=30)
            r.raise_for_status()
            with open(path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            stats[path] = "downloaded"
        except Exception as e:
            stats[path] = f"error: {e}"
    return stats


def detect_objects(image_path: str, model_dir: str, conf_threshold: float = 0.4) -> Dict[str, object]:
    """
    Detect objects using MobileNet-SSD Caffe model.
    model_dir must contain:
      - MobileNetSSD_deploy.prototxt
      - MobileNetSSD_deploy.caffemodel

    Returns a list of detections: {label, confidence, bbox}
    """
    if cv2 is None or np is None:
        return {"error": "opencv-python and numpy required for object detection"}

    proto = os.path.join(model_dir, "MobileNetSSD_deploy.prototxt")
    model = os.path.join(model_dir, "MobileNetSSD_deploy.caffemodel")
    if not (os.path.exists(proto) and os.path.exists(model)):
        return {"error": "model files not found in model_dir; run download_mobilenet_ssd(model_dir)"}

    # Labels for MobileNetSSD
    CLASSES = [
        "background", "aeroplane", "bicycle", "bird", "boat",
        "b
