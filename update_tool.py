import requests
import os
import shutil
from datetime import datetime
import argparse
import subprocess
import sys
import pkg_resources

# === CONFIG ===
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/icitifytechltd/Imgmapon/main/"

FILES_TO_UPDATE = [
    "main.py",
    "analyze_content.py",
    "utils.py",
    "requirements.txt",
    "README.md",
    "version.txt"
]

LOCAL_VERSION_FILE = "version.txt"
BACKUP_FOLDER = "backup"

MIN_TORCH_VERSION = "2.2.0"
MIN_TORCHVISION_VERSION = "0.17.0"
MIN_TORCHAUDIO_VERSION = "2.2.0"

# Fallback essential dependencies (for YOLO and other tools)
ESSENTIAL_PACKAGES = [
    "torch", "torchvision", "torchaudio",
    "pandas", "tqdm", "ultralytics",
    "requests", "opencv-python", "Pillow"
]


def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return "0.0.0"


def get_remote_version():
    try:
        r = requests.get(GITHUB_RAW_BASE + "version.txt")
        r.raise_for_status()
        return r.text.strip()
    except Exception:
        return None


def backup_files(silent=False):
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")
    os.makedirs(backup_path)

    for file in FILES_TO_UPDATE:
        if os.path.exists(file):
            shutil.copy(file, backup_path)
    if not silent:
        print(f"🗂️  Backup completed at '{backup_path}'")


def update_files(silent=False):
    for filename in FILES_TO_UPDATE:
        try:
            url = GITHUB_RAW_BASE + filename
            r = requests.get(url)
            r.raise_for_status()
            with open(filename, "wb") as f:
                f.write(r.content)
            if not silent:
                print(f"✅ Updated {filename}")
        except Exception as e:
            if not silent:
                print(f"❌ Failed to update {filename}: {e}")


def install_dependencies(silent=False):
    """Install or upgrade all dependencies from requirements.txt + missing essentials"""
    if not silent:
        print("📦 Checking and installing dependencies...")

    # 1️⃣ Install from requirements.txt if available
    if os.path.exists("requirements.txt"):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"])
        except subprocess.CalledProcessError as e:
            if not silent:
                print(
                    f"⚠️ Warning: Failed to fully install requirements.txt: {e}")

    # 2️⃣ Ensure essential packages are installed
    for package in ESSENTIAL_PACKAGES:
        try:
            pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            if not silent:
                print(f"⚠️ Missing {package}, installing now...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package])
        else:
            if not silent:
                print(f"✅ {package} is installed and ready")

    if not silent:
        print("✅ All dependencies verified and installed successfully.")


def check_torch_versions(silent=False):
    """Check Torch, TorchVision, Torchaudio versions and upgrade if needed"""
    packages = {
        "torch": MIN_TORCH_VERSION,
        "torchvision": MIN_TORCHVISION_VERSION,
        "torchaudio": MIN_TORCHAUDIO_VERSION
    }
    for pkg, min_ver in packages.items():
        try:
            installed_ver = pkg_resources.get_distribution(pkg).version
            if pkg_resources.parse_version(installed_ver) < pkg_resources.parse_version(min_ver):
                if not silent:
                    print(
                        f"⚠️ {pkg} {installed_ver} is outdated → Upgrading to {min_ver}")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", f"{pkg}>={min_ver}"])
            elif not silent:
                print(f"✅ {pkg} version {installed_ver} OK")
        except pkg_resources.DistributionNotFound:
            if not silent:
                print(f"⚠️ {pkg} missing → Installing {min_ver}")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", f"{pkg}>={min_ver}"])


def restart_imgmapon():
    print("🔄 Restarting IMG MAPON...")
    subprocess.Popen([sys.executable, "main.py"])
    print("✅ IMG MAPON restarted successfully.")


def main():
    parser = argparse.ArgumentParser(description="Update IMG MAPON tool")
    parser.add_argument('--silent', action='store_true',
                        help="Run update silently")
    parser.add_argument('--auto-restart', action='store_true',
                        help="Restart after update")
    args = parser.parse_args()
    silent = args.silent

    if not silent:
        print("🌟 Checking for IMG MAPON updates...")

    local_version = get_local_version()
    remote_version = get_remote_version()

    if not remote_version:
        print("⚠️ Could not reach update server. Exiting.")
        return

    if not silent:
        print(f"Current version: {local_version}")
        print(f"Latest version: {remote_version}")

    if local_version != remote_version or True:  # Always force-check updates
        if not silent:
            print("⚡ Backing up and updating all files...")
        backup_files(silent=silent)
        update_files(silent=silent)
        install_dependencies(silent=silent)
        check_torch_versions(silent=silent)
        if not silent:
            print(f"🎉 Updated successfully to version {remote_version}!")
        if args.auto_restart:
            restart_imgmapon()
    else:
        if not silent:
            print("✅ You already have the latest version.")


if __name__ == "__main__":
    main()
