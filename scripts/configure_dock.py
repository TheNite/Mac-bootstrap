#!/usr/bin/env python3
"""
Dock Configuration Script

Configures macOS Dock preferences using dockutil.
Only adds applications that are actually installed.
"""

import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, load_config, command_exists, run_command


# Common application paths
APP_PATHS = {
    'Finder': '/System/Library/CoreServices/Finder.app',
    'Apps': '/System/Applications/Apps.app',
    'Firefox': '/Applications/Firefox.app',
    'Google Chrome': '/Applications/Google Chrome.app',
    'Brave Browser': '/Applications/Brave Browser.app',
    'PyCharm': '/Applications/PyCharm.app',
    'Messages': '/System/Applications/Messages.app',
    'System Settings': '/System/Applications/System Settings.app',
    '1Password': '/Applications/1Password.app',
    'Discord': '/Applications/Discord.app',
    'iTerm': '/Applications/iTerm.app',
    'iTerm2': '/Applications/iTerm2.app',
    'Sublime Text': '/Applications/Sublime Text.app',
}


def get_app_path(app_name):
    """Get the full path for an application"""
    # Check if we have a known path
    if app_name in APP_PATHS:
        app_path = APP_PATHS[app_name]
        if Path(app_path).exists():
            return app_path

    # Try common patterns
    common_paths = [
        f'/Applications/{app_name}.app',
        f'/System/Applications/{app_name}.app',
        f'/Applications/{app_name}',
    ]

    for path in common_paths:
        if Path(path).exists():
            return path

    return None


def configure_dock():
    """Configure macOS Dock using dockutil"""
    config = load_config()
    Logger.info("Configuring Dock...")

    dock_config = config.get('dock', {})

    # Check if dockutil is installed
    if not command_exists("dockutil"):
        Logger.error("dockutil not installed. Run install_packages.py first to install it.")
        return False

    try:
        # Get desired apps list (in order)
        desired_apps = dock_config.get('apps', ['Apps'])

        Logger.info("Removing all existing Dock items (except Finder)...")
        # Remove all apps except Finder (which can't be removed)
        run_command(["dockutil", "--remove", "all", "--no-restart"], check=False)

        # Add apps in specified order (only if they exist)
        Logger.info("Adding applications to Dock...")
        added_count = 0
        skipped_count = 0

        for app_name in desired_apps:
            app_path = get_app_path(app_name)

            if app_path:
                # Add to dock
                result = run_command([
                    "dockutil", "--add", app_path,
                    "--no-restart"
                ], check=False)

                if result and result.returncode == 0:
                    Logger.success(f"  Added {app_name}")
                    added_count += 1
                else:
                    Logger.warning(f"  Failed to add {app_name}")
            else:
                Logger.warning(f"  {app_name} not installed (skipping)")
                skipped_count += 1

        Logger.success(f"Dock apps: {added_count} added, {skipped_count} skipped")

        # Apply dock settings
        if 'tile_size' in dock_config:
            subprocess.run(
                ['defaults', 'write', 'com.apple.dock', 'tilesize', '-int', str(dock_config['tile_size'])],
                check=True
            )
            Logger.info(f"Set dock tile size to {dock_config['tile_size']}")

        if 'autohide' in dock_config:
            subprocess.run(
                ['defaults', 'write', 'com.apple.dock', 'autohide', '-bool', str(dock_config['autohide']).lower()],
                check=True
            )
            Logger.info(f"Set dock autohide to {dock_config['autohide']}")

        if 'show_recents' in dock_config:
            subprocess.run(
                ['defaults', 'write', 'com.apple.dock', 'show-recents', '-bool', str(dock_config['show_recents']).lower()],
                check=True
            )
            Logger.info(f"Set show recents to {dock_config['show_recents']}")

        # Restart Dock to apply all changes
        Logger.info("Restarting Dock...")
        subprocess.run(['killall', 'Dock'], check=True)

        Logger.success("Dock configured successfully")
        return True

    except Exception as e:
        Logger.error(f"Failed to configure Dock: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("  Dock Configuration")
    print("=" * 60)
    print()
    print("NOTE: This script should be run AFTER all applications are installed.")
    print("It will only add apps that are currently installed on your system.")
    print()

    if not configure_dock():
        sys.exit(1)


if __name__ == "__main__":
    main()
