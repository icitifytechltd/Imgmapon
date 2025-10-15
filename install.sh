#!/bin/bash
# ==========================================================
# 🛰️ IMG MAPON - Installer Script
# Developed by ICITIFY TECH | info@icitifytech.com
# ==========================================================

set -e

echo "=========================================================="
echo "     🛰️  IMG MAPON - Image OSINT & Metadata Extractor     "
echo "=========================================================="
echo "Developed by: ICITIFY TECH"
echo "Contact: info@icitifytech.com"
echo "----------------------------------------------------------"

# Detect Python 3
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Please install Python 3 first."
    exit 1
fi

# Install pip if missing
if ! command -v pip3 &> /dev/null; then
    echo "[+] Installing pip3..."
    apt update && apt install -y python3-pip
fi

# Install dependencies
echo "[+] Installing Python dependencies..."
pip3 install -r requirements.txt --break-system-packages || pip3 install -r requirements.txt

# Make sure project structure exists
if [ ! -f "imgmapon_main.py" ]; then
    echo "[!] Run this installer from the project root folder!"
    echo "Example: ./install.sh"
    exit 1
fi

# Create global executable wrapper
BIN_PATH="/usr/local/bin/imgmapon"
echo "[+] Creating system launcher at $BIN_PATH"

cat << 'EOF' > $BIN_PATH
#!/bin/bash
# Launcher for IMG MAPON
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/imgmapon_main.py" ]; then
    python3 "$SCRIPT_DIR/imgmapon_main.py" "$@"
else
    # If script is installed in /usr/local/bin
    BASE_DIR="/opt/imgmapon"
    python3 "$BASE_DIR/imgmapon_main.py" "$@"
fi
EOF

chmod +x $BIN_PATH

# Move project to /opt/imgmapon for clean structure
echo "[+] Copying project to /opt/imgmapon..."
sudo mkdir -p /opt/imgmapon
sudo cp -r . /opt/imgmapon/

echo "----------------------------------------------------------"
echo "[✅] Installation Complete!"
echo "You can now run IMG MAPON anywhere using:"
echo ""
echo "    imgmapon --file <image.jpg>"
echo "    imgmapon --url <image_url>"
echo ""
echo "Results will show in terminal and can be exported via:"
echo "    --json report.json"
echo ""
echo "----------------------------------------------------------"
echo "🛰️  ICITIFY TECH | info@icitifytech.com"
echo "----------------------------------------------------------"
