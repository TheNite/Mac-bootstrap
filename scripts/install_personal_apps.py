#!/usr/bin/env python3
"""
Personal Applications Installation Script

Installs personal/non-professional applications.
This script is separate from the main professional setup.

Apps included:
- Communication: Discord
- Gaming: Jagex Launcher (OSRS), RuneLite (OSRS), Steam
- Cloud Storage: Google Drive
- Utilities: AppCleaner, Keka (archiver), VeraCrypt (encryption)
- Media: VLC, Handbrake (video converter)
- Remote/Network: AnyDesk, Cyberduck (FTP/SFTP), Wireshark
- System Tools: balenaEtcher (USB imaging)

Usage:
    ./install_personal_apps.py        # Interactive mode (asks for confirmation)
    ./install_personal_apps.py -y     # Skip confirmation prompt
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, run_command, command_exists


# Personal applications to install
PERSONAL_APPS = [
    # Communication & Gaming
    'discord',
    'jagex-launcher',
    'runelite',
    'steam',

    # Cloud Storage
    'google-drive',

    # Utilities
    'appcleaner',
    'keka',
    'veracrypt',

    # Media
    'vlc',
    'handbrake',

    # Remote Access & Network Tools
    'anydesk',
    'cyberduck',
    'wireshark',

    # System Tools
    'balenaetcher',

    # Optional
    # 'spotify',  # Uncomment if needed
]


def install_personal_apps():
    """Install personal applications via Homebrew"""
    Logger.info("Checking personal applications...")

    # Check if brew is installed
    if not command_exists("brew"):
        Logger.error("Homebrew not installed. Run install_homebrew.py first")
        return False

    installed_count = 0
    skipped_count = 0
    for app in PERSONAL_APPS:
        # Check if already installed
        result = run_command(["brew", "list", "--cask", app], check=False, capture_output=True)
        if result and result.returncode == 0:
            Logger.warning(f"  {app} already installed (skipping)")
            skipped_count += 1
        else:
            Logger.info(f"  Installing {app}...")
            install_result = run_command(["brew", "install", "--cask", app], check=False)
            if install_result and install_result.returncode == 0:
                installed_count += 1

    Logger.success(f"Personal apps: {installed_count} installed, {skipped_count} skipped")
    return True


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description="Install personal/non-professional applications",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip confirmation prompt and install automatically"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Personal Applications Installation")
    print("=" * 60)
    print()
    print("This will install personal/non-professional apps:")
    for app in PERSONAL_APPS:
        print(f"  - {app}")
    print()

    # Skip confirmation if -y flag is provided
    if not args.yes:
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            Logger.info("Installation cancelled")
            return

    if not install_personal_apps():
        sys.exit(1)


if __name__ == "__main__":
    main()
