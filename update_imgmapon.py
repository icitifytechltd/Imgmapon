#!/usr/bin/env python3
import subprocess
import os
import sys
import requests
import shutil
from datetime import datetime
import pkg_resources
import threading
import time

# ===================================================
# IMG MAPON Auto Updater (Silent Mode)
# Author: ICITIFY TECH
# Version: 1.1 (2025-10-16)
# ===================================================

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/icitifytechltd/Imgmapon/main/"
FILES_TO_UPDATE = [
    "main.py", "analyze_content.py", "utils.py",
    "requirements.txt", "README.md", "version.txt"
]
LOCAL_VERSION_FILE = "version.txt"
BACKUP_FOLDER = "backup"

MIN_TORCH_VERSION = "2.2.0"
MIN_TORCHVISION_VERSION = "0.17.0"
MIN_TORCHAUDIO_VERSION = "2.2.0"


def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return "0.0.0"


def get_remote_version():
    try:
        r = requests.get(GITHUB_RAW_BASE + "version.txt", timeout=10)
        r.raise_for_status()
        return r.text.strip()
    except Exception:
        return None


def backup_files():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)

    for file in FILES_TO_UPDATE:
        if os.path.exists(file):
            shutil.copy(file, backup_path)


def update_files():
    for filename in FILES_TO_UPDATE:
        try:
            url = GITHUB_RAW_BASE + filename
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            with open(filename, "wb") as f:
                f.write(r.content)
        except Exception:
            pass  # silently ignore failures


def install_dependencies():
    try:
        if os.path.exists("requirements.txt"):
            subprocess.run(
                [sys.executable, "-m", "pip", "install",
                    "--upgrade", "-r", "requirements.txt"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    except Exception:
        pass


def check_torch_versions():
    packages = {
        "torch": MIN_TORCH_VERSION,
        "torchvision": MIN_TORCHVISION_VERSION,
        "torchaudio": MIN_TORCHAUDIO_VERSION
    }
    for pkg, min_ver in packages.items():
        try:
            installed_ver = pkg_resources.get_distribution(pkg).version
            if pkg_resources.parse_version(installed_ver) < pkg_resources.parse_version(min_ver):
                subprocess.run(
                    [sys.executable, "-m", "pip",
                        "install", f"{pkg}>={min_ver}"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
        except pkg_resources.DistributionNotFound:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", f"{pkg}>={min_ver}"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )


def silent_update():
    """Runs the entire update process silently in the background."""
    local_version = get_local_version()
    remote_version = get_remote_version()

    if remote_version and local_version != remote_version:
        backup_files()
        update_files()
        install_dependencies()
        check_torch_versions()
        with open(LOCAL_VERSION_FILE, "w") as f:
            f.write(remote_version)


def run_background_update():
    """Launch updater in a background thread so main app isn't blocked."""
    thread = threading.Thread(target=silent_update, daemon=True)
    thread.start()


if __name__ == "__main__":
    # Start background update without disturbing the user
    run_background_update()

    # Continue running main application
    # Example: launch your tool here
    # subprocess.Popen([sys.executable, "main.py"])
    pass
