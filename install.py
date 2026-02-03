#!/usr/bin/env python3
"""
Install tmux config 
"""

import os
import sys
import shutil
import urllib.request
import argparse
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────

REPO_OWNER = "gc1644"
REPO_NAME = "tmux"
BRANCH = "main"  # change if you use master or another branch
FILENAME = "tmux.conf"

GITHUB_RAW_URL = f"https://github.com/gc1644/tmux"

POSSIBLE_LOCATIONS = [
    Path.home() / ".tmux.conf",
    Path.home() / ".config" / "tmux" / "tmux.conf",
]

# Colors (ANSI)
C = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "reset": "\033[0m",
}

# ──────────────────────────────────────────────────────────────────────────────
def get_target_path() -> Path | None:
    """Find the most appropriate place to install tmux.conf"""
    for loc in POSSIBLE_LOCATIONS:
        if loc.parent.exists():
            return loc
    # Fallback: prefer classic ~/.tmux.conf
    return POSSIBLE_LOCATIONS[0]


def backup_existing(path: Path) -> None:
    if not path.exists():
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.with_suffix(path.suffix + f".bak.{timestamp}")
    shutil.copy2(path, backup_path)
    print(f"{C['yellow']}Backed up existing config → {backup_path}{C['reset']}")


def download_config(url: str) -> str:
    print(f"{C['blue']}Downloading from: {url}{C['reset']}")
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


def install(dry_run: bool = False):
    target = get_target_path()
    if not target:
        print(f"{C['red']}Error: Could not determine install location{C['reset']}")
        sys.exit(1)

    print(f"{C['green']}Target location: {target}{C['reset']}")

    if dry_run:
        print(f"{C['yellow']}DRY RUN — no changes will be made{C['reset']}")
        return

    # Backup if exists
    backup_existing(target)

    # Ensure parent dir exists (for ~/.config/tmux case)
    target.parent.mkdir(parents=True, exist_ok=True)

    # Download and write
    try:
        content = download_config(GITHUB_RAW_URL)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{C['green']}Successfully installed tmux.conf to {target}{C['reset']}")
    except Exception as e:
        print(f"{C['red']}Failed to download/install: {e}{C['reset']}")
        sys.exit(1)

    # Optional: tell user how to reload
    print(f"\n{C['blue']}To apply changes immediately:{C['reset']}")
    print("  tmux source-file " + str(target))
    print("  # or inside tmux session: prefix + r  (your prefix is Ctrl+a)")


def main():
    parser = argparse.ArgumentParser(description="Install tmux config from GitHub", add_help=False)
    parser.add_argument("--dry", action="store_true", help="Dry run (show actions without doing them)")
    parser.add_argument("--help", action="store_true", help="Show this help message")

    args = parser.parse_args()

    if args.help:
        print(__doc__.strip())
        sys.exit(0)

    install(dry_run=args.dry)


if __name__ == "__main__":
    main()
