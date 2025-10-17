#!/usr/bin/env python3
import subprocess
import os
import sys
import time


def main():
    print("🔄 Checking for updates...")

    try:
        # Pull latest changes if it's a Git repository
        if os.path.exists(".git"):
            result = subprocess.run(
                ["git", "pull"],
                capture_output=True, text=True
            )
            print(result.stdout)
            if "Already up to date" not in result.stdout:
                print("✅ Update installed successfully!")
            else:
                print("✅ Already up to date.")
        else:
            print("⚠️ Not a git repository, skipping update.")
    except Exception as e:
        print(f"❌ Update failed: {e}")

    # optional: upgrade pip packages
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade",
                "folium", "geopy", "requests", "torch"],
            check=False
        )
        print("✅ Dependencies updated successfully.")
    except Exception as e:
        print(f"⚠️ Could not update dependencies: {e}")


if __name__ == "__main__":
    main()
