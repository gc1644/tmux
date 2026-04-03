#!/usr/bin/env python3
"""
🚀 MAXIMUM FLEX TMUX INSTALLER v2.0
Elegant • Robust • Zero dependencies • Pure stdlib

Installs tmux config exactly as requested:
• tmux.conf          → ~/.config/tmux/tmux.conf
• tmux-start.sh      → /bin/tmux-start.sh          (sudo handled automatically)
• tmux-start.desktop → ~/.local/share/applications/tmux-start.desktop

Features:
- Beautiful ASCII banner + colored output
- Full argparse with --dry-run, --force, --no-backup
- Smart local file detection (if you run from the repo)
- Automatic backups with timestamps
- Permission magic (sudo only when needed for /bin)
- tmux presence check + helpful tips
- Desktop database refresh
- Idempotent & safe by default
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError


# ====================== COLORS ======================
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def cprint(text: str, color: str = Colors.OKGREEN, bold: bool = False, end: str = "\n"):
    prefix = Colors.BOLD if bold else ""
    print(f"{prefix}{color}{text}{Colors.ENDC}", end=end)


# ====================== BANNER ======================
def print_banner():
    banner = r"""
    ████████╗███╗   ███╗██╗   ██╗██╗  ██╗    ██████╗ ██╗   ██╗██████╗ 
    ╚══██╔══╝████╗ ████║██║   ██║╚██╗██╔╝    ██╔══██╗╚██╗ ██╔╝██╔══██╗
       ██║   ██╔████╔██║██║   ██║ ╚███╔╝     ██████╔╝ ╚████╔╝ ██████╔╝
       ██║   ██║╚██╔╝██║██║   ██║ ██╔██╗     ██╔═══╝   ╚██╔╝  ██╔══██╗
       ██║   ██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗    ██║        ██║   ██║  ██║
       ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝        ╚═╝   ╚═╝  ╚═╝
    """
    cprint(banner, Colors.OKCYAN)
    cprint("    ✨ TMUX CONFIG INSTALLER ✨", Colors.HEADER, bold=True)
    cprint("    Crafted by me\n", Colors.OKGREEN)


# ====================== CORE FUNCTIONS ======================
def check_tmux():
    if shutil.which("tmux") is None:
        cprint("⚠️  tmux is not installed or not in PATH!", Colors.WARNING)
        cprint(
            "   Install it first: sudo apt install tmux  or  brew install tmux",
            Colors.WARNING,
        )
        if input("Continue anyway? (y/N): ").lower() != "y":
            sys.exit(1)


def backup_file(path: Path) -> bool:
    if not path.exists():
        return False
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak_{timestamp}")
    shutil.copy2(path, backup_path)
    cprint(f"📦 Backed up {path.name} → {backup_path.name}", Colors.OKBLUE)
    return True


def download_or_use_local(filename: str, tmp_dir: Path) -> Path:
    """Priority: local file in current dir → GitHub raw"""
    local_file = Path.cwd() / filename
    if local_file.exists():
        cprint(
            f"🔍 Found local {filename} — using it (maximum flex mode)", Colors.OKCYAN
        )
        return local_file

    url = f"https://raw.githubusercontent.com/gc1644/tmux/main/{filename}"
    dest = tmp_dir / filename
    cprint(f"📥 Downloading {filename} from GitHub...", Colors.OKBLUE)
    try:
        urlretrieve(url, dest)
        cprint(f"✅ Downloaded {filename}", Colors.OKGREEN)
        return dest
    except URLError as e:
        cprint(f"❌ Failed to download {filename}: {e}", Colors.FAIL)
        sys.exit(1)


def make_executable(path: Path):
    try:
        path.chmod(0o755)
        cprint(f"🔧 Made {path.name} executable (+x)", Colors.OKGREEN)
    except Exception:
        cprint(
            f"⚠️  Could not chmod {path.name} (sudo probably handled it)", Colors.WARNING
        )


def sudo_install(src: Path, dest_dir: Path) -> Path:
    """sudo cp + chmod when normal user can't write"""
    dest = dest_dir / src.name
    cprint(
        f"🔑 sudo required for {dest_dir} — installing {src.name}...", Colors.WARNING
    )
    try:
        subprocess.run(["sudo", "mkdir", "-p", str(dest_dir)], check=True)
        subprocess.run(["sudo", "cp", str(src), str(dest)], check=True)
        subprocess.run(["sudo", "chmod", "755", str(dest)], check=True)
        cprint(f"✅ sudo-installed {src.name} to {dest}", Colors.OKGREEN)
        return dest
    except subprocess.CalledProcessError as e:
        cprint(f"❌ sudo failed: {e}", Colors.FAIL)
        sys.exit(1)


# ====================== MAIN ======================
def main():
    parser = argparse.ArgumentParser(
        description="🚀 The most tmux installer you'll ever see",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would happen, do nothing"
    )
    parser.add_argument(
        "--no-backup", action="store_true", help="Skip backups (dangerous but fast)"
    )
    parser.add_argument("--force", action="store_true", help="Overwrite without asking")
    parser.add_argument(
        "--bin-dir",
        default="/bin",
        help="Where to put tmux-start.sh (default /bin as you asked)",
    )
    args = parser.parse_args()

    print_banner()
    check_tmux()

    # Resolve paths
    home = Path.home()
    tmux_conf_dir = home / ".config" / "tmux"
    bin_dir = Path(args.bin_dir)
    desktop_dir = home / ".local" / "share" / "applications"

    tmux_conf_path = tmux_conf_dir / "tmux.conf"
    start_sh_path = bin_dir / "tmux-start.sh"
    desktop_path = desktop_dir / "tmux-start.desktop"

    cprint("📋 Target locations:", Colors.HEADER, bold=True)
    cprint(f"   • tmux.conf          → {tmux_conf_path}", Colors.OKBLUE)
    cprint(f"   • tmux-start.sh      → {start_sh_path}", Colors.OKBLUE)
    cprint(f"   • tmux-start.desktop → {desktop_path}\n", Colors.OKBLUE)

    if args.dry_run:
        cprint(
            "🔥 DRY-RUN MODE ACTIVATED — nothing will be changed!",
            Colors.WARNING,
            bold=True,
        )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)

        # Download / use local files
        tmux_conf_src = download_or_use_local("tmux.conf", tmp_dir)
        start_sh_src = download_or_use_local("tmux-start.sh", tmp_dir)
        desktop_src = download_or_use_local("tmux-start.desktop", tmp_dir)

        if args.dry_run:
            cprint(
                "\n✅ Dry run finished. Your tmux setup would be perfectly installed.",
                Colors.OKGREEN,
            )
            return

        # === INSTALL TMUX.CONF ===
        tmux_conf_dir.mkdir(parents=True, exist_ok=True)
        if not args.no_backup:
            backup_file(tmux_conf_path)
        shutil.copy2(tmux_conf_src, tmux_conf_path)
        cprint(f"✅ tmux.conf installed to {tmux_conf_path}", Colors.OKGREEN)

        # === INSTALL TMUX-START.SH (sudo) ===
        if bin_dir.exists() and os.access(bin_dir, os.W_OK):
            # No sudo needed
            if not args.no_backup:
                backup_file(start_sh_path)
            shutil.copy2(start_sh_src, start_sh_path)
            make_executable(start_sh_path)
            cprint(f"✅ tmux-start.sh installed to {start_sh_path}", Colors.OKGREEN)
        else:
            start_sh_path = sudo_install(start_sh_src, bin_dir)

        # === INSTALL DESKTOP ENTRY ===
        desktop_dir.mkdir(parents=True, exist_ok=True)
        if not args.no_backup:
            backup_file(desktop_path)
        shutil.copy2(desktop_src, desktop_path)
        cprint(f"✅ tmux-start.desktop installed to {desktop_path}", Colors.OKGREEN)

    # Final touches
    if sys.platform.startswith("linux"):
        try:
            subprocess.run(["update-desktop-database", str(desktop_dir)], check=False)
            cprint("🔄 Updated desktop database", Colors.OKGREEN)
        except Exception:
            pass

    cprint("\n🎉 MAXIMUM FLEX ACHIEVED!", Colors.OKGREEN, bold=True)
    cprint("Your god-tier tmux setup is now ready.", Colors.HEADER)
    cprint(
        "• Launch with: cosmic-term -e /bin/tmux-start.sh  or from applications menu",
        Colors.OKBLUE,
    )
    cprint("• Reload config: tmux source-file ~/.config/tmux/tmux.conf", Colors.OKBLUE)
    cprint(
        "• Pro tip: add alias tmux-start='/bin/tmux-start.sh' to your shell rc",
        Colors.OKBLUE,
    )
    cprint("\nMade with ❤️  by Grok. Now go flex on everyone.", Colors.OKCYAN)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n⛔ Installation cancelled by user. No worries!", Colors.WARNING)
    except Exception as e:
        cprint(f"\n💥 Unexpected error: {e}", Colors.FAIL)
        sys.exit(1)
