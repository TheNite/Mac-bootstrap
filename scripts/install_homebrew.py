#!/usr/bin/env python3
"""
Homebrew Installation Script

Installs and updates Homebrew package manager
"""

import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, command_exists, run_command


def install_homebrew():
    """Install Homebrew package manager"""
    Logger.info("Installing Homebrew...")

    # Check if already installed
    if command_exists("brew"):
        Logger.warning("Homebrew already installed")
        return True

    try:
        # Install Homebrew
        install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        subprocess.run(install_cmd, shell=True, check=True)
        Logger.success("Homebrew installed")
        return True
    except Exception as e:
        Logger.error(f"Failed to install Homebrew: {e}")
        return False


def update_homebrew():
    """Update Homebrew"""
    Logger.info("Updating Homebrew...")

    if not command_exists("brew"):
        Logger.error("Homebrew not installed")
        return False

    try:
        run_command(["brew", "update"])
        Logger.success("Homebrew updated")
        return True
    except Exception as e:
        Logger.error(f"Failed to update Homebrew: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("  Homebrew Installation")
    print("=" * 60)
    print()

    if install_homebrew():
        update_homebrew()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
