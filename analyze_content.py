# analyze_content.py
# IMG MAPON - Image analysis utilities
# Author: ICITIFY TECH

from PIL import Image, ImageFilter
import cv2
import numpy as np
from sklearn.cluster import KMeans
import pytesseract

# Predefined COCO classes for object detection (already fixed)
CLASSES = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "sofa", "potted plant", "bed", "dining table", "toilet", "tvmonitor",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush"
]

# ---------------------------
# Dominant colors extraction
# ---------------------------


def dominant_colors(image_path, k=5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_flat = img.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(img_flat)
    colors = kmeans.cluster_centers_.astype(int)

    return [tuple(color) for color in colors]

# ---------------------------
# Edge detection
# ---------------------------


def detect_edges(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 100, 200)
    return edges

# ---------------------------
# Basic OCR
# ---------------------------


def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

# ---------------------------
# Utility: Image info
# ---------------------------


def image_info(image_path):
    img = Image.open(image_path)
    return {
        "format": img.format,
        "mode": img.mode,
        "size": img.size
    }

# ---------------------------
# Placeholder for object detection
# ---------------------------


def detect_objects(image_path):
    # Placeholder for YOLO / TensorFlow detection
    return ["person", "dog"]  # Example output
