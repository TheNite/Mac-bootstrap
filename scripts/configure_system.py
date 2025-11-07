#!/usr/bin/env python3
"""
System Preferences Configuration Script

Configures macOS system preferences
"""

import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, load_config


def configure_system():
    """Configure system preferences"""
    config = load_config()
    Logger.info("Configuring system preferences...")

    system_config = config.get('system', {})

    try:
        # Keyboard settings
        if 'key_repeat_rate' in system_config:
            subprocess.run(
                ['defaults', 'write', 'NSGlobalDomain', 'KeyRepeat', '-int', str(system_config['key_repeat_rate'])],
                check=True
            )

        if 'initial_key_repeat' in system_config:
            subprocess.run(
                ['defaults', 'write', 'NSGlobalDomain', 'InitialKeyRepeat', '-int', str(system_config['initial_key_repeat'])],
                check=True
            )

        # Trackpad settings
        if system_config.get('tap_to_click'):
            subprocess.run(
                ['defaults', 'write', 'com.apple.driver.AppleBluetoothMultitouch.trackpad', 'Clicking', '-bool', 'true'],
                check=True
            )
            subprocess.run(
                ['defaults', '-currentHost', 'write', 'NSGlobalDomain', 'com.apple.mouse.tapBehavior', '-int', '1'],
                check=True
            )

        if 'tracking_speed' in system_config:
            subprocess.run(
                ['defaults', 'write', 'NSGlobalDomain', 'com.apple.trackpad.scaling', '-float', str(system_config['tracking_speed'])],
                check=True
            )

        # Text settings
        if system_config.get('disable_auto_correct'):
            subprocess.run(
                ['defaults', 'write', 'NSGlobalDomain', 'NSAutomaticSpellingCorrectionEnabled', '-bool', 'false'],
                check=True
            )

        if system_config.get('disable_auto_capitalize'):
            subprocess.run(
                ['defaults', 'write', 'NSGlobalDomain', 'NSAutomaticCapitalizationEnabled', '-bool', 'false'],
                check=True
            )

        # Screenshot settings
        if 'screenshot_location' in system_config:
            screenshot_dir = Path(system_config['screenshot_location']).expanduser()
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ['defaults', 'write', 'com.apple.screencapture', 'location', '-string', str(screenshot_dir)],
                check=True
            )

        if 'screenshot_show_thumbnail' in system_config:
            subprocess.run(
                ['defaults', 'write', 'com.apple.screencapture', 'show-thumbnail', '-bool',
                 str(system_config['screenshot_show_thumbnail']).lower()],
                check=True
            )

        Logger.success("System preferences configured")
        return True

    except Exception as e:
        Logger.error(f"Failed to configure system preferences: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("  System Preferences Configuration")
    print("=" * 60)
    print()

    if not configure_system():
        sys.exit(1)


if __name__ == "__main__":
    main()
