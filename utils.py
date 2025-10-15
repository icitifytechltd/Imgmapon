
import os
import json
---

# 🧠 Code separation

# 1️⃣ **utils.py**
```python


def banner():
    print(r"""
██╗███╗   ███╗ ██████╗     ███╗   ███╗ █████╗ ██████╗  ██████╗ ███╗   ██╗
██║████╗ ████║██╔═══██╗    ████╗ ████║██╔══██╗██╔══██╗██╔═══██╗████╗  ██║
██║██╔████╔██║██║   ██║    ██╔████╔██║███████║██████╔╝██║   ██║██╔██╗ ██║
██║██║╚██╔╝██║██║   ██║    ██║╚██╔╝██║██╔══██║██╔══██╗██║   ██║██║╚██╗██║
██║██║ ╚═╝ ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╔╝██║ ╚████║
╚═╝╚═╝     ╚═╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                    Developed by ICITIFY TECH  |  info@icitifytech.com
""")


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[+] JSON report saved to {os.path.abspath(path)}")
