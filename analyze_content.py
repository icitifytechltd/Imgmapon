# analyze_content.py
# IMG MAPON - Image analysis utilities (Production)
# Author: ICITIFY TECH

from PIL import Image, ExifTags
import cv2
import numpy as np
from sklearn.cluster import KMeans
import pytesseract
import torch

# Predefined COCO classes for object detection
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
    return edges.tolist()  # JSON-friendly

# ---------------------------
# OCR Text extraction
# ---------------------------


def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


# ---------------------------
# Object detection using YOLOv5
# ---------------------------
# Load model once for production
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


def detect_objects(image_path):
    results = yolo_model(image_path)
    objects = []
    for *box, conf, cls in results.xyxy[0]:
        objects.append({
            "class": yolo_model.names[int(cls)],
            "confidence": float(conf),
            "box": [float(x) for x in box]
        })
    return objects

# ---------------------------
# Image info / Metadata extraction
# ---------------------------


def image_info(image_path):
    img = Image.open(image_path)
    info = {
        "format": img.format,
        "mode": img.mode,
        "size": img.size
    }

    # Extract EXIF metadata if available
    exif_data = {}
    try:
        raw_exif = img._getexif()
        if raw_exif:
            for tag, value in raw_exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                exif_data[decoded] = value
    except Exception:
        exif_data = {}

    info["exif"] = exif_data

    # Optional: extract GPS info if available
    gps_info = {}
    if "GPSInfo" in exif_data:
        gps_raw = exif_data["GPSInfo"]
        gps_info = {ExifTags.GPSTAGS.get(k, k): v for k, v in gps_raw.items()}
    info["gps"] = gps_info

    return info
