Got it! Here’s a **ready-to-copy `README.md` file** you can paste directly into your project:

---

````markdown
# IMG MAPON

**IMG MAPON** is a powerful image intelligence tool developed by **ICITIFY TECH**.  
It extracts metadata, detects objects, finds dominant colors, edges, and performs OCR from images or image URLs.  

---

## Features

- Extract image metadata (format, size, mode)  
- Detect dominant colors in an image  
- Perform edge detection  
- Extract text using OCR  
- Object detection (placeholder for YOLO/TensorFlow)  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ICITIFYTECH/Imgmapon.git
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

---

## Usage

Run the main script:

```bash
python imgmapon_main.py --help
```

### Available Commands

| Command                | Description                               |
| ---------------------- | ----------------------------------------- |
| `--image <image_path>` | Analyze a local image file                |
| `--url <image_url>`    | Analyze an image from a URL               |
| `--metadata`           | Extract image metadata                    |
| `--colors`             | Detect dominant colors                    |
| `--edges`              | Perform edge detection                    |
| `--text`               | Extract text from image using OCR         |
| `--objects`            | Detect objects in the image (placeholder) |

### Examples

Analyze a local image:

```bash
python imgmapon_main.py --image example.jpg --metadata --colors --edges --text --objects
```

Analyze an image from a URL:

```bash
python imgmapon_main.py --url https://example.com/image.jpg --metadata --colors --edges --text --objects
```

This will output:

* Metadata (format, size, mode)
* Dominant colors
* Edge detection image (saved locally)
* Extracted text
* Detected objects

---

## Requirements

* Python 3.13+
* pip packages (see `requirements.txt`)
* Tesseract OCR

---

## Author

**ICITIFY TECH**
Email: [info@icitifytech.com](mailto:info@icitifytech.com)

```

---

If you want, I can **also make a fully working `imgmapon_main.py` script** that exactly supports all these commands and outputs results nicely—so after pasting the README, the tool works immediately.  

Do you want me to do that next?
```
