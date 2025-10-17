#!/usr/bin/env python3
import subprocess
import os
import sys
import threading
import time


MAIN_APP = "main.py"  # your main application file


def background_update():
    """Perform git and dependency updates silently, then restart main app."""
    updated = False

    # --- Git update ---
    if os.path.exists(".git"):
        try:
            result = subprocess.run(
                ["git", "pull"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            if "Already up to date" not in result.stdout:
                updated = True
        except Exception:
            pass

    # --- Pip dependencies update ---
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade",
             "folium", "geopy", "requests", "torch"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        updated = True
    except Exception:
        pass

    # --- Restart main application if updated ---
    if updated and os.path.exists(MAIN_APP):
        try:
            subprocess.Popen([sys.executable, MAIN_APP],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        except Exception:
            pass


def run_background_update():
    """Run the updater in a non-blocking background thread."""
    thread = threading.Thread(target=background_update, daemon=True)
    thread.start()


if __name__ == "__main__":
    run_background_update()

    # --- Start your main app normally if not handled by updater ---
    if os.path.exists(MAIN_APP):
        subprocess.Popen([sys.executable, MAIN_APP])
