#!/usr/bin/env python3
# =========================================================
# IMG MAPON v1.1 — Advanced Image Forensics Tool (Maps)
# Created by ICITIFY TECH
# =========================================================

import argparse
import os
import sys
import time
import json
import socket
import subprocess
import requests
from PIL import Image
from io import BytesIO
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import re
import html

# Local modules
from img_utils import banner, save_json
from analyze_content import dominant_colors, detect_edges, extract_text, detect_objects, image_info
# keep import pattern compatible
from extract_metadata import extract_metadata


# NOTE: if you actually use extract_metadata, adjust the import above.
# Map filename
MAP_FILENAME = "imgmapon_map.html"


# =========================================================
# AUTO-UPDATE + AUTO-RESTART
# =========================================================
def auto_update_and_restart():
    try:
        result = subprocess.run(
            [sys.executable, "update_tool.py", "--silent"],
            capture_output=True, text=True
        )
        if any(word in result.stdout for word in ["✅", "Updated", "installed", "successfully"]):
            print("\n🔁 Update detected! Restarting IMG MAPON...\n")
            subprocess.Popen([sys.executable, "main.py"])
            sys.exit(0)
    except Exception as e:
        print(f"⚠️ Auto-update skipped: {e}")


auto_update_and_restart()


# =========================================================
# BANNER
# =========================================================
def welcome_banner():
    banner_lines = [
        "██████╗ ██╗███╗   ███╗ ███╗   ███╗ █████╗ ██████╗ ███╗   ██╗",
        "██╔══██╗██║████╗ ████║ ████╗ ████║██╔══██╗██╔═══██╗████╗  ██║",
        "██████╔╝██║██╔████╔██║ ██╔████╔██║███████║██║   ██║██╔██╗ ██║",
        "██╔═══╝ ██║██║╚██╔╝██║ ██║╚██╔╝██║██╔══██║██║   ██║██║╚██╗██║",
        "██║     ██║██║ ╚═╝ ██║ ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║ ╚████║",
        "╚═╝     ╚═╝╚═╝     ╚═╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝",
        "                   WELCOME TO IMG MAPON v1.1",
        "             Mapping & Dual-Location Intelligence",
        "                   Created by ICITIFY TECH"
    ]
    colors = ['\033[91m', '\033[93m', '\033[92m',
              '\033[96m', '\033[94m', '\033[95m']
    reset = '\033[0m'
    for idx, line in enumerate(banner_lines):
        color = colors[idx % len(colors)]
        for char in line:
            print(f"{color}{char}{reset}", end="", flush=True)
            time.sleep(0.0015)
        print()
        time.sleep(0.05)


# =========================================================
# HELPERS (SMART URL RESOLUTION + DOWNLOAD)
# =========================================================
def _extract_google_photos_direct_link(html_text):
    """
    Try to find an lh*.googleusercontent.com link inside Google Photos share page.
    """
    # unescape HTML then search
    txt = html.unescape(html_text)
    # pattern: https://lhX.googleusercontent.com/...
    match = re.search(
        r'(https:\/\/lh\d+\.googleusercontent\.com\/[^\s"\'<>]+)', txt)
    if match:
        return match.group(1)
    return None


def _resolve_google_drive(url):
    """
    Convert various Google Drive share formats to a direct download link (if public).
    Examples:
      - https://drive.google.com/file/d/FILEID/view?usp=sharing
      - https://drive.google.com/uc?export=download&id=FILEID
    Returns direct url or None.
    """
    # file/d/FILEID
    m = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if m:
        file_id = m.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    # open?id=FILEID
    m = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
    if m:
        file_id = m.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return None


def _resolve_dropbox(url):
    """
    Convert Dropbox share links to direct dl=1 links.
    """
    # Dropbox share link has dl=0 or ?dl=0; convert to dl=1
    if "dropbox.com" in url:
        if "dl=0" in url:
            return url.replace("dl=0", "dl=1")
        if "dl=1" not in url:
            if "?" in url:
                return url + "&dl=1"
            else:
                return url + "?dl=1"
    return None


def _resolve_imgur(url):
    """
    Convert Imgur page links to direct image (.jpg) links when possible.
    - https://imgur.com/abcd -> https://i.imgur.com/abcd.jpg
    - https://i.imgur.com/abcd.jpg stays as is
    """
    if "i.imgur.com" in url:
        return url
    m = re.search(r'imgur\.com/(?:gallery/|a/)?([A-Za-z0-9]+)', url)
    if m:
        img_id = m.group(1)
        return f"https://i.imgur.com/{img_id}.jpg"
    return None


def download_image(url, save_path="temp_image.jpg"):
    """
    Robust downloader that:
      - resolves Google Photos, Drive, Dropbox, Imgur public links
      - sets browser-like headers
      - retries a few times and reports clear errors
    """
    if not url:
        print("❌ No URL provided.")
        return None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Quick helpers to try multiple candidate URLs (resolved)
    candidate_urls = [url]

    # Google Drive
    gd = _resolve_google_drive(url)
    if gd and gd not in candidate_urls:
        candidate_urls.append(gd)

    # Dropbox
    db = _resolve_dropbox(url)
    if db and db not in candidate_urls:
        candidate_urls.append(db)

    # Imgur
    im = _resolve_imgur(url)
    if im and im not in candidate_urls:
        candidate_urls.append(im)

    # Google Photos: try resolving the page first to extract the direct lh* URL
    if "photos.app.goo.gl" in url or "googleusercontent.com" in url and "photos" in url:
        try:
            session = requests.Session()
            resp = session.get(url, headers=headers, timeout=15)
            if resp.status_code == 200 and resp.text:
                direct = _extract_google_photos_direct_link(resp.text)
                if direct:
                    if direct not in candidate_urls:
                        candidate_urls.insert(0, direct)  # prefer direct link
                else:
                    # Sometimes Google Photos page contains meta tags with image links
                    meta_match = re.search(
                        r'<meta property="og:image" content="([^"]+)"', resp.text)
                    if meta_match:
                        meta_url = meta_match.group(1)
                        if meta_url not in candidate_urls:
                            candidate_urls.insert(0, meta_url)
        except Exception:
            pass

    # Try all candidate URLs with retries
    last_err = None
    for candidate in candidate_urls:
        for attempt in range(3):
            try:
                # Some hosts block requests without Referer; set Referer to candidate domain
                headers_local = headers.copy()
                try:
                    headers_local["Referer"] = "/".join(
                        candidate.split("/")[:3])
                except Exception:
                    pass

                resp = requests.get(
                    candidate, headers=headers_local, stream=True, timeout=20)
                # handle common client errors quickly
                if resp.status_code == 403:
                    last_err = f"403 Forbidden for url: {candidate}"
                    # try next candidate or retry
                    time.sleep(1)
                    continue
                if resp.status_code == 404:
                    last_err = f"404 Not Found for url: {candidate}"
                    break  # no point retrying 404 on same URL
                resp.raise_for_status()

                # Check content-type to ensure it's an image
                ctype = resp.headers.get("Content-Type", "")
                if not ctype.startswith("image/"):
                    # maybe it's an HTML page (private link). If so, try to parse for direct image
                    text = resp.text or ""
                    direct = _extract_google_photos_direct_link(text)
                    if direct and direct != candidate:
                        candidate = direct
                        continue
                    last_err = f"URL did not return image content-type ({ctype}) for: {candidate}"
                    break

                # Save the image
                with open(save_path, "wb") as f:
                    for chunk in resp.iter_content(1024):
                        if chunk:
                            f.write(chunk)
                return save_path

            except requests.exceptions.HTTPError as he:
                last_err = f"HTTP error ({he.response.status_code}) for {candidate}"
                # 404 -> break, 403 -> retry, others -> retry
                if he.response.status_code == 404:
                    break
                time.sleep(1)
                continue
            except requests.exceptions.RequestException as rexc:
                last_err = f"Network error for {candidate}: {rexc}"
                time.sleep(1)
                continue
            except Exception as exc:
                last_err = f"Unexpected error for {candidate}: {exc}"
                time.sleep(1)
                continue

    # all candidates exhausted
    if last_err:
        print(f"❌ Error downloading image: {last_err}")
    else:
        print("❌ Error downloading image: Unknown error.")
    return None


def get_host_ip(url):
    try:
        host = url.split("//")[-1].split("/")[0]
        return socket.gethostbyname(host)
    except Exception:
        return None


def ip_to_geolocation(ip):
    """Enhanced IP location finder with multiple fallback APIs."""
    if not ip:
        return None
    services = [
        f"https://ipapi.co/{ip}/json/",
        f"https://ipinfo.io/{ip}/json",
        f"http://ip-api.com/json/{ip}"
    ]
    for svc in services:
        try:
            res = requests.get(svc, timeout=10)
            res.raise_for_status()
            data = res.json()
            # normalize keys across services
            lat = data.get("latitude") or (data.get("loc", "").split(
                ",")[0] if data.get("loc") else None) or data.get("lat")
            lon = data.get("longitude") or (data.get("loc", "").split(
                ",")[1] if data.get("loc") else None) or data.get("lon")
            return {
                "ip": ip,
                "city": data.get("city") or data.get("regionName"),
                "region": data.get("region") or data.get("regionName"),
                "country": data.get("country_name") or data.get("country"),
                "latitude": lat,
                "longitude": lon,
                "org": data.get("org") or data.get("isp")
            }
        except Exception:
            continue
    return None


# =========================================================
# GPS HANDLING
# =========================================================
def convert_to_degrees(value):
    try:
        d, m, s = value
        return d[0]/d[1] + (m[0]/m[1])/60.0 + (s[0]/s[1])/3600.0
    except Exception:
        return None


def gps_to_location(gps_data):
    """Smart reverse GPS lookup with retries and fallback geocoders."""
    if not gps_data or "GPSLatitude" not in gps_data or "GPSLongitude" not in gps_data:
        return None
    try:
        lat = convert_to_degrees(gps_data["GPSLatitude"])
        lon = convert_to_degrees(gps_data["GPSLongitude"])
        if gps_data.get("GPSLatitudeRef") == "S":
            lat = -lat
        if gps_data.get("GPSLongitudeRef") == "W":
            lon = -lon
        # primary geolocator
        geolocator = Nominatim(user_agent="imgmapon_locator", timeout=10)
        for attempt in range(3):
            try:
                location = geolocator.reverse((lat, lon), language="en")
                if location:
                    return {
                        "latitude": lat,
                        "longitude": lon,
                        "address": location.address,
                        "country": location.raw.get("address", {}).get("country", "Unknown"),
                        "city": location.raw.get("address", {}).get("city", "Unknown")
                    }
            except Exception:
                time.sleep(1)
        # fallback: geocode.xyz
        try:
            resp = requests.get(
                f"https://geocode.xyz/{lat},{lon}?json=1", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "latitude": lat,
                    "longitude": lon,
                    "address": data.get("staddress", "Unknown"),
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown")
                }
        except Exception:
            pass
        return {"latitude": lat, "longitude": lon, "address": "Not found"}
    except Exception as e:
        return {"error": f"GPS decoding failed: {e}"}


# =========================================================
# MAP GENERATION (Folium)
# =========================================================
def generate_map(data, map_filename=MAP_FILENAME):
    """
    Create an interactive folium map showing:
     - photo GPS location (if available)
     - IP/server location (if available)
     - polyline between points and distance label
    Saves HTML file and returns path or None on failure.
    """
    try:
        import folium
    except Exception:
        print("⚠️ folium not installed. To enable map generation, run: pip install folium")
        return None

    gps_info = data.get("gps_location")
    ip_info = data.get("ip_location")

    if not gps_info and not ip_info:
        return None

    coords = []
    if gps_info and isinstance(gps_info, dict) and gps_info.get("latitude") and gps_info.get("longitude"):
        try:
            coords.append(
                (float(gps_info["latitude"]), float(gps_info["longitude"])))
        except Exception:
            pass
    if ip_info and ip_info.get("latitude") and ip_info.get("longitude"):
        try:
            coords.append(
                (float(ip_info["latitude"]), float(ip_info["longitude"])))
        except Exception:
            pass

    if not coords:
        return None

    avg_lat = sum(c[0] for c in coords) / len(coords)
    avg_lon = sum(c[1] for c in coords) / len(coords)
    m = folium.Map(location=[avg_lat, avg_lon],
                   zoom_start=5, control_scale=True)

    if gps_info and gps_info.get("latitude") and gps_info.get("longitude"):
        folium.Marker(
            location=[float(gps_info["latitude"]),
                      float(gps_info["longitude"])],
            popup=folium.Popup(
                f"Photo location:<br>{gps_info.get('address', 'N/A')}", max_width=400),
            tooltip="Photo GPS location",
            icon=folium.Icon(color="blue", icon="camera")
        ).add_to(m)

    if ip_info and ip_info.get("latitude") and ip_info.get("longitude"):
        folium.Marker(
            location=[float(ip_info["latitude"]), float(ip_info["longitude"])],
            popup=folium.Popup(
                f"Server/IP location:<br>{ip_info.get('ip')}<br>{ip_info.get('org', '')}", max_width=400),
            tooltip="Image host/server location",
            icon=folium.Icon(color="red", icon="cloud")
        ).add_to(m)

    if len(coords) >= 2:
        folium.PolyLine(coords, color="green",
                        weight=2.5, opacity=0.8).add_to(m)
        try:
            distance_km = geodesic(coords[0], coords[1]).kilometers
            mid = ((coords[0][0]+coords[1][0])/2,
                   (coords[0][1]+coords[1][1])/2)
            folium.Marker(
                location=mid,
                icon=folium.DivIcon(
                    html=f"""<div style="font-size:12px;color:green;background:rgba(255,255,255,0.8);padding:4px;border-radius:4px">Distance: {distance_km:.2f} km</div>""")
            ).add_to(m)
            data["_map_distance_km"] = distance_km
        except Exception:
            pass

    try:
        m.fit_bounds(m.get_bounds())
    except Exception:
        pass

    try:
        m.save(map_filename)
        return os.path.abspath(map_filename)
    except Exception:
        return None


# =========================================================
# CORE PROCESSING
# =========================================================
def process_image(image_path, args):
    results = {}
    if args.metadata:
        meta = image_info(image_path)
        results["metadata"] = meta
        gps = meta.get("gps", {})
        results["gps"] = gps
        results["gps_location"] = gps_to_location(gps)
    if args.colors:
        colors = dominant_colors(image_path)
        results["dominant_colors"] = [tuple(map(int, c)) for c in colors]
    if args.edges:
        edges = detect_edges(image_path)
        results["edges"] = edges.tolist() if hasattr(
            edges, 'tolist') else edges
    if args.text:
        text = extract_text(image_path)
        results["text"] = text
    if args.objects:
        objects = detect_objects(image_path)
        results["objects"] = objects
    if args.search:
        results["reverse_search"] = "🔍 Feature under development"
    if args.research:
        results["deep_research"] = "🧠 Feature under development"
    return results


# =========================================================
# MAIN
# =========================================================
def main():
    welcome_banner()
    time.sleep(0.8)
    banner()

    parser = argparse.ArgumentParser(
        description="IMG MAPON - Advanced Image Forensics Tool")
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
    parser.add_argument('--map', action='store_true',
                        help="Generate interactive map HTML (folium)")
    args = parser.parse_args()

    if args.image:
        image_path = args.image
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            return
        results = {"source": "local", "image_path": image_path}
        # local machine IP for origin (best-effort)
        try:
            ip = requests.get("https://ipapi.co/ip/", timeout=5).text.strip()
        except Exception:
            ip = None
    elif args.url:
        image_path = download_image(args.url)
        if not image_path:
            return
        host_ip = get_host_ip(args.url)
        results = {"source": "url", "image_url": args.url, "host_ip": host_ip}
        ip = host_ip
    else:
        print("⚠️ Please provide --image or --url.")
        return

    data = process_image(image_path, args)
    data.update(results)

    # Always include IP-based location (even if GPS exists)
    ip_info = ip_to_geolocation(ip)
    if ip_info:
        data["ip_location"] = ip_info

    # Save JSON results
    try:
        # Support save_json signature either (filename, data) or (data, filename)
        # try both to be safe
        try:
            save_json("imgmapon_results.json", data)
        except TypeError:
            save_json(data, "imgmapon_results.json")
    except Exception as e:
        print(f"⚠️ Could not save JSON results: {e}")
    else:
        print("\n✅ Results saved to imgmapon_results.json\n")

    # Generate map if requested
    map_path = None
    if args.map:
        map_path = generate_map(data)
        if map_path:
            print(f"🗺️ Map generated: {map_path}")
            if "_map_distance_km" in data:
                print(
                    f"📏 Distance between photo and host: {data['_map_distance_km']:.2f} km")
        else:
            print("⚠️ Map was not generated (missing folium or no valid coords).")

    # Terminal summary
    print("\n========================================================")
    print("🧠 ANALYSIS SUMMARY")
    print("========================================================")
    meta = data.get("metadata", {})
    print(f"📸 Format: {meta.get('format', 'Unknown')}")
    print(f"🎨 Mode: {meta.get('mode', 'Unknown')}")
    print(f"📏 Size: {meta.get('size', 'Unknown')}")

    gps_info = data.get("gps_location")
    if gps_info:
        print("\n🗺️ Photo GPS Location:")
        print(f"   📍 {gps_info.get('address', 'N/A')}")
        print(
            f"   🌍 Lat/Lon: {gps_info.get('latitude')}, {gps_info.get('longitude')}")
        print(
            f"   🏙️ City: {gps_info.get('city')} | Country: {gps_info.get('country')}")

    if "ip_location" in data:
        ip_loc = data["ip_location"]
        print("\n💻 Image Origin Server/IP Location:")
        print(f"   🌐 IP: {ip_loc.get('ip')} ({ip_loc.get('org', 'Unknown')})")
        print(
            f"   🏙️ City: {ip_loc.get('city')} | {ip_loc.get('region')} | {ip_loc.get('country')}")
        print(
            f"   📍 Lat/Lon: {ip_loc.get('latitude')}, {ip_loc.get('longitude')}")
    else:
        print("\n💻 IP-based Location: Not available")

    if "objects" in data:
        objects = data["objects"]
        if objects:
            print(f"\n🧩 Detected Objects ({len(objects)}):")
            for obj in objects:
                if isinstance(obj, dict):
                    print(
                        f"   - {obj.get('class', '?')} ({obj.get('confidence', 0):.2f})")
                else:
                    print(f"   - {obj}")
        else:
            print("\n🧩 Detected Objects: None")
    else:
        print("\n🧩 Detected Objects: N/A")

    if "text" in data:
        text_data = data["text"]
        if text_data:
            print("\n🔠 Extracted Text:")
            print(f"   {text_data[:500]}")
        else:
            print("\n🔠 Extracted Text: None")
    else:
        print("\n🔠 Extracted Text: N/A")

    print("\n========================================================")
    if map_path:
        print(f"🗺️ Map file: {map_path} (open in browser)")
    print("✅ Results also saved as 'imgmapon_results.json'")
    print("========================================================\n")


if __name__ == "__main__":
    main()
