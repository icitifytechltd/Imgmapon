import requests
import os
import shutil
from datetime import datetime
import argparse
import subprocess
import sys
import pkg_resources

# ===================================================
# IMG MAPON Auto Updater
# Author: ICITIFY TECH
# Version: 1.1 (2025-10-16)
# ===================================================

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


def backup_files(silent=False):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)

    for file in FILES_TO_UPDATE:
        if os.path.exists(file):
            shutil.copy(file, backup_path)
    if not silent:
        print(f"🗂️  Backup completed at '{backup_path}'")


def update_files(silent=False):
    for filename in FILES_TO_UPDATE:
        try:
            url = GITHUB_RAW_BASE + filename
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            with open(filename, "wb") as f:
                f.write(r.content)
            if not silent:
                print(f"✅ Updated {filename}")
        except Exception as e:
            if not silent:
                print(f"❌ Failed to update {filename}: {e}")


def install_dependencies(silent=False):
    if not os.path.exists("requirements.txt"):
        if not silent:
            print("⚠️ requirements.txt not found. Skipping dependency check.")
        return
    if not silent:
        print("📦 Installing/upgrading dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install",
                "--upgrade", "-r", "requirements.txt"]
        )
        if not silent:
            print("✅ Dependencies installed/updated successfully.")
    except subprocess.CalledProcessError as e:
        if not silent:
            print(f"❌ Failed to install dependencies: {e}")


def check_torch_versions(silent=False):
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
                        f"⚠️ {pkg} {installed_ver} outdated. Upgrading to {min_ver}...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip",
                        "install", f"{pkg}>={min_ver}"]
                )
            elif not silent:
                print(f"✅ {pkg} version {installed_ver} is OK")
        except pkg_resources.DistributionNotFound:
            if not silent:
                print(f"⚠️ {pkg} is missing. Installing {min_ver}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", f"{pkg}>={min_ver}"]
            )


def restart_imgmapon():
    print("🔄 Restarting IMG MAPON...")
    subprocess.Popen([sys.executable, "main.py"])
    print("✅ IMG MAPON restarted successfully.")


def main():
    parser = argparse.ArgumentParser(description="Update IMG MAPON tool")
    parser.add_argument('--silent', action='store_true',
                        help="Run update silently")
    parser.add_argument('--auto-restart', action='store_true',
                        help="Restart IMG MAPON after update")
    args = parser.parse_args()

    silent = args.silent

    if not silent:
        print("🌟 Checking for updates for IMG MAPON...")

    local_version = get_local_version()
    remote_version = get_remote_version()

    if not remote_version:
        if not silent:
            print("⚠️ Could not check for updates. Please try again later.")
        return

    if not silent:
        print(f"Current version: {local_version}")
        print(f"Latest version: {remote_version}")

    if local_version != remote_version:
        if not silent:
            print("⚡ New version detected! Backing up current files...")
        backup_files(silent)
        if not silent:
            print("⚡ Updating all files...")
        update_files(silent)
        install_dependencies(silent)
        check_torch_versions(silent)
        with open(LOCAL_VERSION_FILE, "w") as f:
            f.write(remote_version)
        if not silent:
            print(f"🎉 IMG MAPON updated to version {remote_version}!")
        if args.auto_restart:
            restart_imgmapon()
    else:
        if not silent:
            print("✅ You already have the latest version.")


if __name__ == "__main__":
    main()
