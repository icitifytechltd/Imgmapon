import argparse
import os
import json
import socket
from PIL import Image
from extract_metadata import extract_metadata
from analyze_content import dominant_colors, detect_edges, extract_text, detect_objects, image_info
from utils import banner, save_json
import requests
from io import BytesIO
from geopy.geocoders import Nominatim  # for reverse geolocation from GPS
# Welcome Massage

import time
import sys


def welcome_banner():
    banner_lines = [
        "██████╗ ██╗███╗   ███╗ ███╗   ███╗ █████╗ ██████╗ ███╗   ██╗",
        "██╔══██╗██║████╗ ████║ ████╗ ████║██╔══██╗██╔═══██╗████╗  ██║",
        "██████╔╝██║██╔████╔██║ ██╔████╔██║███████║██║   ██║██╔██╗ ██║",
        "██╔═══╝ ██║██║╚██╔╝██║ ██║╚██╔╝██║██╔══██║██║   ██║██║╚██╗██║",
        "██║     ██║██║ ╚═╝ ██║ ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║ ╚████║",
        "╚═╝     ╚═╝╚═╝     ╚═╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝",
        "                   WELCOME TO IMG MAPON v2",
        "                Advanced Image Forensics Tool",
        "                   Created by ICITIFY TECH"
    ]

    # ANSI color codes for a gradient effect
    colors = [
        '\033[91m',  # Red
        '\033[93m',  # Yellow
        '\033[92m',  # Green
        '\033[96m',  # Cyan
        '\033[94m',  # Blue
        '\033[95m',  # Magenta
    ]

    reset = '\033[0m'

    for idx, line in enumerate(banner_lines):
        color = colors[idx % len(colors)]  # cycle colors
        for char in line:
            print(f"{color}{char}{reset}", end="", flush=True)
            time.sleep(0.0015)  # Typing effect speed
        print()
        time.sleep(0.05)  # Pause betwee


# -------------------
# Helper Functions
# -------------------


def download_image(url, save_path="temp_image.jpg"):
    """Download image from URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return save_path
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


def get_host_ip(url):
    """Get IP address of image host."""
    try:
        host = url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(host)
        return ip
    except Exception as e:
        return f"Unknown ({e})"


def gps_to_location(gps):
    """Convert GPS info to human-readable location."""
    if not gps:
        return None
    try:
        geolocator = Nominatim(user_agent="imgmapon")
        lat = gps.get("GPSLatitude")
        lon = gps.get("GPSLongitude")
        if lat and lon:
            location = geolocator.reverse((lat, lon), language="en")
            return location.address if location else None
    except Exception as e:
        return f"Unknown ({e})"

# -------------------
# Core Image Processing
# -------------------


def process_image(image_path, args):
    results = {}

    # Metadata + EXIF
    if args.metadata:
        meta = image_info(image_path)
        results["metadata"] = meta
        gps = meta.get("gps", {})
        results["gps"] = gps
        results["gps_location"] = gps_to_location(gps)

    # Dominant colors
    if args.colors:
        colors = dominant_colors(image_path)
        results["dominant_colors"] = [tuple(map(int, c)) for c in colors]

    # Edge detection
    if args.edges:
        edges = detect_edges(image_path)
        results["edges"] = edges.tolist() if hasattr(
            edges, 'tolist') else edges

    # Text extraction
    if args.text:
        text = extract_text(image_path)
        results["text"] = text

    # Object detection
    if args.objects:
        objects = detect_objects(image_path)
        results["objects"] = objects

    # Reverse image search placeholder
    if args.search:
        results["reverse_search"] = "Feature under development"

    # Deep research placeholder
    if args.research:
        results["deep_research"] = "Feature under development"

    return results

# -------------------
# My Main Function
# -------------------


def main():
    banner()

    parser = argparse.ArgumentParser(
        description="IMG MAPON - Advanced Image Forensics Tool"
    )
    parser.add_argument('--image', type=str, help="Path to the image file")
    parser.add_argument('--url', type=str, help="URL of the image")
    parser.add_argument('--metadata', action='store_true',
                        help="Extract metadata")
    parser.add_argument('--colors', action='store_true',
                        help="Detect dominant colors")
    parser.add_argument('--edges', action='store_true',
                        help="Perform edge detection")
    parser.add_argument('--text', action='store_true',
                        help="Extract text using OCR")
    parser.add_argument('--objects', action='store_true',
                        help="Detect objects")
    parser.add_argument('--search', action='store_true',
                        help="Reverse image search")
    parser.add_argument('--research', action='store_true',
                        help="Conduct deep research")
    args = parser.parse_args()

    # Decide image source
    if args.image:
        image_path = args.image
        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            return
        results = {"source": "local", "image_path": image_path}
    elif args.url:
        image_path = download_image(args.url)
        if not image_path:
            return
        results = {"source": "url", "image_url": args.url,
                   "host_ip": get_host_ip(args.url)}
    else:
        print("Please provide --image or --url.")
        return

    # Process image
    data = process_image(image_path, args)

    # Merge source info
    data.update(results)

    # Where result is save into
    save_json("imgmapon_results.json", data)
    print("\n✅ Results saved to imgmapon_results.json\n")


def check_version():
    current_version = "v2.0.1"
    try:
        r = requests.get(
            "https://raw.githubusercontent.com/icitifytechltd/Imgmapon/main/version.txt")
        latest_version = r.text.strip()
        if latest_version != current_version:
            print(f"⚠️ Update available: {latest_version}")
    except:
        print("⚠️ Could not check latest version")


# -------------------
if __name__ == "__main__":
    main()
