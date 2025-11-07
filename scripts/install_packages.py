#!/usr/bin/env python3
"""
Package Installation Script

Installs Homebrew formulae, casks, and fonts
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, load_config, run_command, command_exists


def install_packages():
    """Install Homebrew formulae, casks, and fonts"""
    config = load_config()

    Logger.info("Installing Homebrew packages...")

    # Check if brew is installed
    if not command_exists("brew"):
        Logger.error("Homebrew not installed. Run install_homebrew.py first")
        return False

    # Tap font cask if fonts are needed
    fonts = config.get('brew_fonts', [])
    if fonts:
        Logger.info("Tapping homebrew/cask-fonts...")
        run_command(["brew", "tap", "homebrew/cask-fonts"], check=False)

    # Install formulae (CLI tools)
    formulae = config.get('brew_formulae', [])
    if formulae:
        Logger.info(f"Checking {len(formulae)} formulae...")
        installed_count = 0
        skipped_count = 0
        for formula in formulae:
            # Check if already installed
            result = run_command(["brew", "list", formula], check=False, capture_output=True)
            if result and result.returncode == 0:
                Logger.warning(f"  {formula} already installed (skipping)")
                skipped_count += 1
            else:
                Logger.info(f"  Installing {formula}...")
                install_result = run_command(["brew", "install", formula], check=False)
                if install_result and install_result.returncode == 0:
                    installed_count += 1
        Logger.success(f"Formulae: {installed_count} installed, {skipped_count} skipped")

    # Install fonts
    if fonts:
        Logger.info(f"Checking {len(fonts)} fonts...")
        installed_count = 0
        skipped_count = 0
        for font in fonts:
            # Check if already installed
            result = run_command(["brew", "list", "--cask", font], check=False, capture_output=True)
            if result and result.returncode == 0:
                Logger.warning(f"  {font} already installed (skipping)")
                skipped_count += 1
            else:
                Logger.info(f"  Installing {font}...")
                install_result = run_command(["brew", "install", "--cask", font], check=False)
                if install_result and install_result.returncode == 0:
                    installed_count += 1
        Logger.success(f"Fonts: {installed_count} installed, {skipped_count} skipped")

    # Install casks (GUI apps)
    casks = config.get('brew_casks', [])
    if casks:
        Logger.info(f"Checking {len(casks)} casks...")
        installed_count = 0
        skipped_count = 0
        for cask in casks:
            # Check if already installed
            result = run_command(["brew", "list", "--cask", cask], check=False, capture_output=True)
            if result and result.returncode == 0:
                Logger.warning(f"  {cask} already installed (skipping)")
                skipped_count += 1
            else:
                Logger.info(f"  Installing {cask}...")
                install_result = run_command(["brew", "install", "--cask", cask], check=False)
                if install_result and install_result.returncode == 0:
                    installed_count += 1
        Logger.success(f"Casks: {installed_count} installed, {skipped_count} skipped")

    Logger.success("Homebrew packages installed")
    return True


def main():
    """Main execution"""
    print("=" * 60)
    print("  Package Installation")
    print("=" * 60)
    print()

    if not install_packages():
        sys.exit(1)


if __name__ == "__main__":
    main()
