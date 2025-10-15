import argparse
import tempfile
import requests
import os
from utils import banner, save_json
from extract_metadata import extract_exif, gps_from_exif
from analyze_content import dominant_colors, detect_edges
from reverse_lookup import reverse_image_search


def download_image(url):
    r = requests.get(url, timeout=5)
    tmp_path = os.path.join(tempfile.gettempdir(), "imgmapon_tmp.jpg")
    with open(tmp_path, "wb") as f:
        f.write(r.content)
    return tmp_path


def main():
    parser = argparse.ArgumentParser(
        description="IMG MAPON — Image OSINT Analysis")
    parser.add_argument("--file", help="Local image path")
    parser.add_argument("--url", help="Remote image URL")
    parser.add_argument("--json", help="Save JSON report")
    args = parser.parse_args()

    banner()

    if not args.file and not args.url:
        parser.error("Specify --file or --url")

    if args.url:
        print(f"[+] Downloading image from: {args.url}")
        path = download_image(args.url)
    else:
        path = args.file

    print(f"[+] Analyzing: {path}")

    data = {}
    exif = extract_exif(path)
    gps = gps_from_exif(exif)
    data["metadata"] = exif
    data["gps"] = gps
    data["colors"] = dominant_colors(path)
    data["edge_density"] = detect_edges(path)

    if args.url:
        data["reverse_lookup"] = reverse_image_search(args.url)

    print("\n--- Summary ---")
    for k, v in data.items():
        print(f"{k}: {v}")

    if args.json:
        save_json(data, args.json)


if __name__ == "__main__":
    main()
