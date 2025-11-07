#!/usr/bin/env python3
"""
Finder Configuration Script

Configures macOS Finder preferences
"""

import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, load_config


def configure_finder():
    """Configure Finder preferences"""
    config = load_config()
    Logger.info("Configuring Finder...")

    finder_config = config.get('finder', {})

    try:
        # View style mapping
        view_styles = {
            'icon': 'icnv',
            'list': 'Nlsv',
            'column': 'clmv',
            'gallery': 'glyv'
        }

        default_view = finder_config.get('default_view', 'list')
        if default_view in view_styles:
            subprocess.run(
                ['defaults', 'write', 'com.apple.finder', 'FXPreferredViewStyle', '-string', view_styles[default_view]],
                check=True
            )

        if finder_config.get('show_path_bar'):
            subprocess.run(
                ['defaults', 'write', 'com.apple.finder', 'ShowPathbar', '-bool', 'true'],
                check=True
            )

        if finder_config.get('show_status_bar'):
            subprocess.run(
                ['defaults', 'write', 'com.apple.finder', 'ShowStatusBar', '-bool', 'true'],
                check=True
            )

        if finder_config.get('show_hidden_files'):
            subprocess.run(
                ['defaults', 'write', 'com.apple.finder', 'AppleShowAllFiles', '-bool', 'true'],
                check=True
            )

        # Restart Finder
        subprocess.run(['killall', 'Finder'], check=True)
        Logger.success("Finder configured")
        return True

    except Exception as e:
        Logger.error(f"Failed to configure Finder: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("  Finder Configuration")
    print("=" * 60)
    print()

    if not configure_finder():
        sys.exit(1)


if __name__ == "__main__":
    main()
