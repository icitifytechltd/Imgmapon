````markdown
# IMG MAPON v2 - Advanced Image Forensics Tool

**Author:** ICITIFY TECH  
**Email:** info@icitifytech.com  

IMG MAPON is an advanced image forensics tool designed for deep image analysis, including metadata extraction, object detection, OCR, color analysis, and more. It supports both local images and images from URLs.

---

## Features

- Extract **image metadata** (EXIF info, GPS coordinates, camera model, etc.)  
- Convert **GPS data to human-readable location**  
- Detect **dominant colors** in the image  
- Perform **edge detection** for image analysis  
- Extract **text using OCR**  
- Detect **objects** (YOLO-based placeholder detection included)  
- Support for **reverse image search** (planned)  
- Support for **deep research / AI integration** (planned)  
- Works with **local images** or **downloaded from URL**  
- Outputs results in a **JSON file** for easy processing  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/icitifytechltd/Imgmapon.git
cd imgmapon
````

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Basic usage:

Analyze a local image:

```bash
python main.py --image path/to/image.jpg --metadata --colors --edges --text --objects
```

Analyze an image from a URL:

```bash
python main.py --url https://example.com/image.jpg --metadata --colors --edges
```

### Options

| Argument     | Description                                       |
| ------------ | ------------------------------------------------- |
| `--image`    | Path to the local image file                      |
| `--url`      | URL of the image                                  |
| `--metadata` | Extract metadata (EXIF, GPS, camera)              |
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

## Output Example

```json
{
  "metadata": {
    "format": "JPEG",
    "mode": "RGB",
    "size": [1024, 768],
    "gps": {
      "GPSLatitude": 40.7128,
      "GPSLongitude": -74.0060
    }
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
  "source": "local",
  "image_path": "test_image.jpg"
}
```

---

## License

This project is licensed under the **MIT License**.
See `LICENSE` for details.

---

## Notes

* Ensure **Tesseract OCR** is installed and accessible for text extraction.
* For GPS location, **geopy** uses OpenStreetMap Nominatim API, which requires an internet connection.
* Object detection is currently a placeholder; integrate **YOLOv5** or similar models for full functionality.

---

**ICITIFY TECH** – Secure, deep, and intelligent image analysis.

```