#!/usr/bin/env python3
"""
Zsh and Oh My Zsh Installation Script

Installs Oh My Zsh and custom plugins
"""

import os
import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, load_config


def install_oh_my_zsh():
    """Install Oh My Zsh framework"""
    Logger.info("Installing Oh My Zsh...")

    # Check if already installed
    oh_my_zsh_dir = Path.home() / '.oh-my-zsh'
    if oh_my_zsh_dir.exists():
        Logger.warning("Oh My Zsh already installed")
        return True

    try:
        # Download and install Oh My Zsh (non-interactive)
        install_cmd = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended'
        subprocess.run(install_cmd, shell=True, check=True)
        Logger.success("Oh My Zsh installed")

        # Set zsh as default shell
        current_shell = os.environ.get('SHELL', '')
        if 'zsh' not in current_shell:
            Logger.info("Setting zsh as default shell...")
            subprocess.run(['chsh', '-s', '/bin/zsh'], check=False)
            Logger.success("Zsh set as default shell (restart terminal to apply)")

        return True
    except Exception as e:
        Logger.error(f"Failed to install Oh My Zsh: {e}")
        return False


def install_zsh_plugins():
    """Install custom Zsh plugins"""
    Logger.info("Installing custom Zsh plugins...")

    custom_plugins_dir = Path.home() / '.oh-my-zsh' / 'custom' / 'plugins'
    custom_plugins_dir.mkdir(parents=True, exist_ok=True)

    plugins_to_install = {
        'zsh-autosuggestions': 'https://github.com/zsh-users/zsh-autosuggestions',
        'zsh-syntax-highlighting': 'https://github.com/zsh-users/zsh-syntax-highlighting',
        'zsh-interactive-cd': 'https://github.com/changyuheng/zsh-interactive-cd',
        'you-should-use': 'https://github.com/MichaelAquilina/zsh-you-should-use',
        'zsh-bat': 'https://github.com/fdellwing/zsh-bat'
    }

    success_count = 0
    for plugin_name, repo_url in plugins_to_install.items():
        plugin_path = custom_plugins_dir / plugin_name
        if plugin_path.exists():
            Logger.warning(f"{plugin_name} already installed")
            success_count += 1
        else:
            try:
                subprocess.run(
                    ['git', 'clone', repo_url, str(plugin_path)],
                    check=True,
                    capture_output=True
                )
                Logger.success(f"Installed {plugin_name}")
                success_count += 1
            except Exception as e:
                Logger.error(f"Failed to install {plugin_name}: {e}")

    Logger.success(f"Zsh plugins installation complete ({success_count}/{len(plugins_to_install)})")
    return success_count == len(plugins_to_install)


def main():
    """Main execution"""
    config = load_config()
    optional_config = config.get('optional', {})

    print("=" * 60)
    print("  Zsh and Oh My Zsh Installation")
    print("=" * 60)
    print()

    if not optional_config.get('install_oh_my_zsh'):
        Logger.info("Oh My Zsh installation disabled in config")
        return

    if install_oh_my_zsh():
        install_zsh_plugins()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
