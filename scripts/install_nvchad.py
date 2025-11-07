#!/usr/bin/env python3
"""
NvChad Installation Script

Installs NvChad configuration for Neovim
"""

import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, load_config


def install_nvchad():
    """Install NvChad for Neovim"""
    Logger.info("Installing NvChad...")

    nvim_config_dir = Path.home() / '.config' / 'nvim'

    if nvim_config_dir.exists():
        Logger.warning("Neovim config already exists. Skipping NvChad installation.")
        Logger.info(f"To reinstall, backup and remove: {nvim_config_dir}")
        return False

    try:
        # Clone NvChad starter config
        install_cmd = 'git clone https://github.com/NvChad/starter ~/.config/nvim'
        subprocess.run(install_cmd, shell=True, check=True)
        Logger.success("NvChad installed")
        Logger.info("Run 'nvim' to complete NvChad setup (plugins will auto-install)")
        return True

    except Exception as e:
        Logger.error(f"Failed to install NvChad: {e}")
        return False


def main():
    """Main execution"""
    config = load_config()
    optional_config = config.get('optional', {})

    print("=" * 60)
    print("  NvChad Installation")
    print("=" * 60)
    print()

    if not optional_config.get('install_nvchad'):
        Logger.info("NvChad installation disabled in config")
        return

    install_nvchad()


if __name__ == "__main__":
    main()
