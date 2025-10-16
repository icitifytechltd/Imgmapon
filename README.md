```markdown
# IMG MAPON v2 - Advanced Image Forensics & Deep Image Analysis Tool

**Author:** ICITIFY TECH  
**Email:** info@icitifytech.com  

IMG MAPON v2 is a powerful, production-ready image forensics tool designed for **deep image analysis**. It provides metadata extraction, GPS location lookup, object detection, OCR, color analysis, edge detection, and more. It supports both **local images** and **images from URLs** and now integrates host IP detection and enhanced data insights.

---

## Key Features in v2

- **Metadata Extraction:** EXIF info, GPS coordinates, camera model, and other image details.  
- **GPS to Location:** Converts GPS coordinates into human-readable locations using OpenStreetMap.  
- **Dominant Color Detection:** Detects top colors present in the image using KMeans clustering.  
- **Edge Detection:** Highlights edges for visual analysis.  
- **Text Extraction (OCR):** Extracts text from images using Tesseract.  
- **Object Detection:** YOLO-based detection placeholder (can be replaced with full YOLOv5/YOLOv8 models).  
- **Image Source Info:** Identifies if the image is local or downloaded, including host IP for URL images.  
- **Reverse Image Search:** Placeholder for future integration with reverse search engines.  
- **Deep Research / AI Analysis:** Placeholder for integrating AI tools like Google Gemini or ExaAI for deep image insights.  
- **JSON Output:** All results saved in a structured JSON file for easy parsing.  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/icitifytechltd/Imgmapon.git
cd imgmapon
````

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** v2 now requires `torch`, `torchvision`, and `torchaudio` for object detection. These are included in `requirements.txt`.

---

## Usage

### Local Image Analysis:

```bash
python main.py --image path/to/image.jpg --metadata --colors --edges --text --objects
```

### Image from URL:

```bash
python main.py --url https://example.com/image.jpg --metadata --colors --edges
```

### Available Options:

| Argument     | Description                                       |
| ------------ | ------------------------------------------------- |
| `--image`    | Path to the local image file                      |
| `--url`      | URL of the image                                  |
| `--metadata` | Extract metadata (EXIF, GPS, camera model)        |
| `--colors`   | Detect dominant colors                            |
| `--edges`    | Perform edge detection                            |
| `--text`     | Extract text using OCR                            |
| `--objects`  | Detect objects in the image                       |
| `--search`   | Perform reverse image search (coming soon)        |
| `--research` | Conduct deep research / AI analysis (coming soon) |

### Example Command:

```bash
python main.py --image test_image.jpg --metadata --colors --edges --text --objects
```

After running, results are saved in:

```
imgmapon_results.json
```

---

## Sample JSON Output

```json
{
  "metadata": {
    "format": "JPEG",
    "mode": "RGB",
    "size": [1024, 768],
    "gps": {
      "GPSLatitude": 40.7128,
      "GPSLongitude": -74.0060
    },
    "camera": "Canon EOS 80D"
  },
  "gps_location": "New York, NY, USA",
  "dominant_colors": [
    [77, 80, 84],
    [189, 183, 183],
    [122, 60, 52]
  ],
  "edges": [[255, 0, 255, ...]],
  "text": "Sample text extracted from image",
  "objects": ["person", "dog"],
  "source": "url",
  "image_url": "https://example.com/image.jpg",
  "host_ip": "93.184.216.34"
}
```

---

## Notes & Requirements

* **Tesseract OCR** must be installed and accessible for text extraction.
* **Geopy / OpenStreetMap** requires an internet connection for GPS-to-location conversion.
* Object detection is currently a placeholder; integrate **YOLOv5/YOLOv8** for full object detection functionality.
* Reverse image search and AI-based deep research are planned features in upcoming versions.

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

**ICITIFY TECH** – Secure, intelligent, and deep image analysis for production environments.

```