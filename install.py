#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess
from urllib.request import urlretrieve

h = Path.home()
d = h / ".config/tmux"
d.mkdir(parents=True, exist_ok=True)

for f in ["tmux.conf", "tmux-start.sh", "tmux-start.desktop"]:
    u = f"https://raw.githubusercontent.com/gc1644/tmux/main/{f}"
    s = Path(f) if Path(f).exists() else urlretrieve(u, f)[0]

    if f == "tmux.conf":
        shutil.copy2(s, d / "tmux.conf")
        print("✓ tmux.conf")

    elif f == "tmux-start.sh":
        p = Path("/bin") / f
        if p.parent.writable():
            shutil.copy2(s, p)
            p.chmod(0o755)
        else:
            subprocess.run(["sudo", "cp", s, p], check=True)
            subprocess.run(["sudo", "chmod", "755", p], check=True)
        print("✓ tmux-start.sh")

    else:
        shutil.copy2(s, h / ".local/share/applications" / f)
        print("✓ tmux-start.desktop")

subprocess.run(
    ["update-desktop-database", str(h / ".local/share/applications")],
    stdout=-1,
    stderr=-1,
)

print("Done.")
