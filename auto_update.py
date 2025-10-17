#!/usr/bin/env python3
import subprocess
import os
import time
import sys
from threading import Thread


def safe_git_pull(timeout=10):
    """Safely pull updates from git without hanging the terminal."""
    if not os.path.exists(".git"):
        print("⚠️ No .git repository found — skipping update.")
        return

    print("🔄 Checking for updates...")
    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if "Already up to date" in result.stdout:
            print("✅ Already up to date.")
        else:
            print("✅ Repository updated successfully.")
    except subprocess.TimeoutExpired:
        print("⚠️ Git update check timed out — skipping.")
    except Exception as e:
        print(f"⚠️ Update failed: {e}")


def auto_update_once_per_day(force=False):
    """Run update check only once every 24 hours, unless forced."""
    last_check = "/tmp/last_git_check"
    one_day = 86400  # 24 hours in seconds

    if force:
        print("🚀 Forcing manual update check...")
        Thread(target=safe_git_pull, daemon=True).start()
        return

    if not os.path.exists(last_check) or time.time() - os.path.getmtime(last_check) > one_day:
        open(last_check, "w").close()
        Thread(target=safe_git_pull, daemon=True).start()
    else:
        print("⏩ Skipping auto-update (checked within 24 hours).")


def main():
    # Handle optional command-line flags
    force_update = "--update" in sys.argv or "--force-update" in sys.argv

    # Run safe background update logic
    auto_update_once_per_day(force=force_update)

    # Continue with your main tool logic
    print("🚀 Starting tool... (terminal remains responsive)")


if __name__ == "__main__":
    main()
