### 📄 Updated `README.md`

````markdown
# IMG MAPON

**IMG MAPON** is a powerful image intelligence tool developed by **ICITIFY TECH**.  
It extracts metadata, detects objects, finds dominant colors, edges, and performs OCR from images or image URLs. Additionally, it offers advanced features for deep image research and easy lookups.

## Features

- Extract image metadata (format, size, mode)
- Detect dominant colors in an image
- Perform edge detection
- Extract text using OCR
- Object detection (placeholder for YOLO/TensorFlow)
- Reverse image search using AI-powered tools
- Deep research capabilities for comprehensive analysis

## Installation

1. Clone the repository:

```bash
git clone https://github.com/icitifytechltd/Imgmapon.git
cd Imgmapon
````

2. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
sudo apt update
sudo apt install -y python3-pip tesseract-ocr libtesseract-dev
pip install -r requirements.txt
```

## Usage

Run the main script:

```bash
python imgmapon_main.py --help
```

### Available Commands

| Command          | Description                        |
| ---------------- | ---------------------------------- |
| `--image <path>` | Analyze a local image file         |
| `--url <url>`    | Analyze an image from a URL        |
| `--metadata`     | Extract image metadata             |
| `--colors`       | Detect dominant colors             |
| `--edges`        | Perform edge detection             |
| `--text`         | Extract text from image using OCR  |
| `--objects`      | Detect objects in the image        |
| `--search`       | Perform reverse image search       |
| `--research`     | Conduct deep research on the image |

### Examples

Analyze a local image:

```bash
python imgmapon_main.py --image example.jpg --metadata --colors --edges --text --objects --search --research
```

Analyze an image from a URL:

```bash
python imgmapon_main.py --url https://example.com/image.jpg --metadata --colors --edges --text --objects --search --research
```

This will output:

* Metadata (format, size, mode)
* Dominant colors
* Edge detection image (saved locally)
* Extracted text
* Detected objects
* Reverse image search results
* Deep research findings

## Requirements

* Python 3.13+
* pip packages (see `requirements.txt`)
* Tesseract OCR

## License

**IMG MAPON** is proprietary software.

Copyright (c) 2025 **ICITIFY TECH**
Email: [info@icitifytech.com](mailto:info@icitifytech.com)

All rights reserved. You may use this software for personal or internal purposes only. Redistribution, selling, or claiming ownership of IMG MAPON or its derivative works is prohibited without explicit permission from ICITIFY TECH.

## Author

**ICITIFY TECH**
Email: [info@icitifytech.com](mailto:info@icitifytech.com)

```

---

By implementing these enhancements, **IMG MAPON** will become a more robust tool for deep image research and easy lookups, providing users with comprehensive insights and analysis capabilities. If you need assistance with integrating these features into your existing codebase or have any questions, feel free to ask!
::contentReference[oaicite:21]{index=21}
 
```