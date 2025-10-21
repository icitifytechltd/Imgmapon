

██╗███╗   ███╗ ████╗   ████╗ ████╗   ███╗ ████╗ ██████╗ ██╗███╗   ██╗
██║████╗ ████║ ██╔██╗ ██╔██╗ ████║ ██╔██╗ ██╔██╗ ██╔══██╗██║████╗  ██║
██║██╔████╔██║ ██║╚██╗██║╚██╗██╔██║ ██║╚██╗██║╚██╗██║  ██║██║██╔██╗ ██║
██║██║╚██╔╝██║ ██║ ╚███║ ╚███║██║ ██║ ██║ ╚███║ ╚██║  ██║██║██║╚██╗██║
██║██║ ╚═╝ ██║ ██║  ╚══╝  ╚══╝██║ ██║ ██║  ╚══╝  ╚██████╔╝██║██║ ╚████║
╚═╝╚═╝     ╚═╝ ╚═╝         ╚═╝╚═╝ ╚═╝ ╚═╝         ╚═════╝ ╚═╝╚═╝  ╚═══╝

---

````markdown
# 🛰️ IMG MAPON v1.1  
### Advanced Image Forensics & Deep Intelligence Tool  

![Version](https://img.shields.io/badge/version-1.1-blue.svg)
![Status](https://img.shields.io/badge/build-stable-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Made by](https://img.shields.io/badge/made%20by-ICITIFY%20TECH-purple.svg)

---

**Author:** ICITIFY TECH  
**Email:** info@icitifytech.com  
**License:** MIT  
**Version:** 1.1 (Advanced Edition)

---

## 🔍 Overview

**IMG MAPON v1.1** by **ICITIFY TECH** is a powerful and intelligent **image forensics tool** that extracts deep insights from digital images.  
It analyzes **metadata**, **GPS**, **EXIF**, **objects**, **text**, and **geolocation** — then displays it all in an elegant, interactive report and HTML map.

Built for:
- 🕵️‍♂️ Digital Forensics Experts  
- 🔒 Cybersecurity Analysts  
- 🤖 AI Researchers  
- 🧠 Data Intelligence Developers  

---

## ✨ Key Features (v1.1)

| Category | Description |
|----------|--------------|
| 🧭 **Location Intelligence** | GPS decoding + IP geolocation + AI fallback |
| 🧠 **Object Detection** | YOLOv5 detection with class + confidence |
| 🔤 **Text Extraction (OCR)** | Reads visible words using Tesseract |
| 🎨 **Visual Analytics** | Dominant colors + edge detection |
| 🗺️ **Mapping Intelligence** | Generates HTML maps linking GPS + IP |
| 🔁 **Auto-Updater** | `update_tool.py` keeps your tool fresh |
| 🧩 **Modular Analysis** | Choose exactly what to analyze |
| 📜 **JSON Export** | Full structured output for API or reporting |

---

## ⚡ Quick Start

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/icitifytechltd/Imgmapon.git
cd Imgmapon
python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
pip install -r requirements.txt
````

> Optional for AI/YOLO detection:
>
> ```bash
> pip install torch torchvision torchaudio
> ```

---

## 🚀 Usage

### Local Image

```bash
python main.py --image test.jpg --metadata --colors --objects --map
```

### Online Image

```bash
python main.py --url https://example.com/image.jpg --metadata --map
```

### Google Photos Link

```bash
python main.py --url https://photos.app.goo.gl/your-photo-link --metadata --map
```

### Update Tool

```bash
python main.py --update
or 
python auto_update.py

```

---

## 🧠 Sample Output (JSON)

```json
{
  "metadata": {
    "format": "JPEG",
    "camera": "Samsung S22",
    "size": [3024, 4032]
  },
  "gps_location": {
    "latitude": 6.5244,
    "longitude": 3.3792,
    "address": "Lagos, Nigeria"
  },
  "ip_location": {
    "ip": "142.250.184.206",
    "city": "Frankfurt",
    "country": "Germany"
  },
  "dominant_colors": ["#2F2F2F", "#9E9E9E", "#E1E1E1"],
  "objects": [{"name": "person", "confidence": 0.97}],
  "text": "PRIVATE PROPERTY",
  "source": "url"
}
```

---

## 🧭 Command Options

| Argument     | Description                                      |
| ------------ | ------------------------------------------------ |
| `--image`    | Analyze a local image                            |
| `--url`      | Analyze an online image (supports Google Photos) |
| `--metadata` | Extract EXIF, GPS, and image format              |
| `--colors`   | Detect dominant colors                           |
| `--edges`    | Run edge detection                               |
| `--text`     | Extract text using OCR                           |
| `--objects`  | Run YOLOv5 detection                             |
| `--map`      | Generate interactive HTML map                    |
| `--search`   | Reverse image search *(coming soon)*             |
| `--research` | Deep AI image research *(coming soon)*           |

---

## 🗺️ Visual Examples (Assets Folder)
COMING SOON...

 ```

---

## 🧱 Build Executable (Optional)

To generate a standalone version:

```bash
pyinstaller --onefile main.py
```

✅ Output: `dist/main` (Linux/Mac) or `main.exe` (Windows)

---

## ⚙️ Requirements

| Component      | Minimum                       |
| -------------- | ----------------------------- |
| Python         | 3.8+                          |
| Tesseract      | Installed globally for OCR    |
| Torch / YOLOv5 | Required for object detection |
| Internet       | Needed for GPS & IP lookups   |

---

---

## 📜 License

**IMG MAPON v1.1** © 2025 **ICITIFY TECH**
Licensed under **MIT License**
For enterprise builds or private licensing, contact: **[info@icitifytech.com](mailto:info@icitifytech.com)**

---

## 💡 Credits

Created & maintained by **ICITIFY TECH**
🌍 [https://icitifytech.com](https://icitifytech.com)
🧠 Digital Forensics | AI Security | Deep Image Analytics
🚀 *Empowering cyber intelligence through image data.*

---