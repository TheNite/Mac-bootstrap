#!/usr/bin/env python3
"""
Dotfiles Copy Script

Copies dotfiles to home directory
"""

import shutil
import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, load_config


def copy_dotfiles():
    """Copy dotfiles to home directory"""
    Logger.info("Copying dotfiles...")

    try:
        # Get project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        dotfiles_dir = project_root / 'dotfiles'

        if not dotfiles_dir.exists():
            Logger.warning("Dotfiles directory not found")
            return False

        # Copy all zsh config files
        zsh_files = ['.zshrc', '.zsh_aliases', '.zsh_functions']
        copied_count = 0

        for zsh_file in zsh_files:
            src = dotfiles_dir / zsh_file
            dst = Path.home() / zsh_file

            if not src.exists():
                Logger.warning(f"{zsh_file} not found in dotfiles directory")
                continue

            # Backup existing file if it exists
            if dst.exists():
                timestamp = subprocess.run(
                    ['date', '+%Y%m%d%H%M%S'],
                    capture_output=True,
                    text=True
                ).stdout.strip()
                backup_path = Path.home() / f"{zsh_file}.backup.{timestamp}"
                shutil.copy2(dst, backup_path)
                Logger.info(f"Backed up existing {zsh_file} to {backup_path.name}")

            shutil.copy2(src, dst)
            Logger.success(f"Copied {zsh_file}")
            copied_count += 1

        if copied_count > 0:
            Logger.success(f"Dotfiles copied ({copied_count}/{len(zsh_files)})")
            return True
        else:
            Logger.warning("No dotfiles were copied")
            return False

    except Exception as e:
        Logger.error(f"Failed to copy dotfiles: {e}")
        return False


def main():
    """Main execution"""
    config = load_config()
    optional_config = config.get('optional', {})

    print("=" * 60)
    print("  Dotfiles Copy")
    print("=" * 60)
    print()

    if not optional_config.get('copy_dotfiles'):
        Logger.info("Dotfiles copy disabled in config")
        return

    if not copy_dotfiles():
        sys.exit(1)


if __name__ == "__main__":
    main()
