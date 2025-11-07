#!/usr/bin/env python3
"""
macOS Fresh Install Setup Tool - Main Orchestrator

This is the main entry point that orchestrates all setup scripts.
Each component is handled by a dedicated microservice-style script.

Usage:
    ./setup.py                  # Run full setup
    ./setup.py --brew-only      # Install only Homebrew packages
    ./setup.py --config-only    # Only apply system configurations
    ./setup.py --dotfiles-only  # Only copy dotfiles
"""

import argparse
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'


class Logger:
    """Simple logger"""

    @staticmethod
    def info(msg):
        print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

    @staticmethod
    def success(msg):
        print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")

    @staticmethod
    def warning(msg):
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")

    @staticmethod
    def error(msg):
        print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")


class SetupOrchestrator:
    """Main orchestrator for setup scripts"""

    def __init__(self):
        self.scripts_dir = Path(__file__).parent / 'scripts'

    def run_script(self, script_name, description):
        """Run a setup script"""
        Logger.info(f"{description}...")

        script_path = self.scripts_dir / f"{script_name}.py"
        if not script_path.exists():
            Logger.error(f"Script not found: {script_path}")
            return False

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                check=True
            )
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            Logger.error(f"Script failed: {script_name}")
            return False
        except Exception as e:
            Logger.error(f"Error running {script_name}: {e}")
            return False

    def run_full_setup(self):
        """Run complete setup process"""
        print("═" * 60)
        print("  macOS Fresh Install Setup")
        print("═" * 60)
        print()

        # Ask for sudo password upfront
        Logger.info("This script requires sudo access...")
        subprocess.run(["sudo", "-v"], check=True)

        # Define setup steps
        steps = [
            ("install_homebrew", "Installing Homebrew"),
            ("install_packages", "Installing packages"),
            ("configure_finder", "Configuring Finder"),
            ("configure_system", "Configuring system preferences"),
            ("configure_git", "Configuring Git"),
            ("install_zsh", "Installing Zsh and Oh My Zsh"),
            ("install_nvchad", "Installing NvChad"),
            ("copy_dotfiles", "Copying dotfiles"),
            ("configure_dock", "Configuring Dock"),  # Last step - only adds installed apps
        ]

        # Execute each step
        for script_name, description in steps:
            if not self.run_script(script_name, description):
                if input(f"\nContinue anyway? (y/n): ").lower() != 'y':
                    sys.exit(1)
            print()  # Blank line between steps

        print("═" * 60)
        Logger.success("macOS setup complete!")
        print("═" * 60)
        print()
        print("Manual steps remaining:")
        print("  1. Sign in to 1Password and sync passwords")
        print("  2. Run 'nvim' to complete NvChad setup")
        print("  3. Configure SSH keys:")
        print("     ssh-keygen -t ed25519 -C \"your_email@example.com\"")
        print("  4. Set up VS Code Settings Sync")
        print("  5. Install browsers manually (Chrome, Firefox, Arc)")
        print("  6. Restart your Mac for all changes to take effect")
        print("  7. Open iTerm2 and set JetBrains Mono Nerd Font")
        print()

    def run_brew_only(self):
        """Install only Homebrew and packages"""
        Logger.info("Running Homebrew-only installation...")
        self.run_script("install_homebrew", "Installing Homebrew")
        self.run_script("install_packages", "Installing packages")

    def run_config_only(self):
        """Apply only system configurations"""
        Logger.info("Applying system configurations only...")
        self.run_script("configure_finder", "Configuring Finder")
        self.run_script("configure_system", "Configuring system preferences")
        self.run_script("configure_git", "Configuring Git")
        self.run_script("configure_dock", "Configuring Dock")  # Last - only adds installed apps

    def run_dotfiles_only(self):
        """Copy only dotfiles"""
        Logger.info("Copying dotfiles only...")
        self.run_script("copy_dotfiles", "Copying dotfiles")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="macOS Fresh Install Setup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./setup.py                  Run full setup
  ./setup.py --brew-only      Install only Homebrew and packages
  ./setup.py --config-only    Apply only system configurations
  ./setup.py --dotfiles-only  Copy only dotfiles

Individual scripts can also be run directly:
  ./scripts/install_homebrew.py
  ./scripts/configure_dock.py
  etc.
        """
    )

    parser.add_argument(
        "--brew-only",
        action="store_true",
        help="Install only Homebrew and packages"
    )
    parser.add_argument(
        "--config-only",
        action="store_true",
        help="Apply only system configurations"
    )
    parser.add_argument(
        "--dotfiles-only",
        action="store_true",
        help="Copy only dotfiles"
    )

    args = parser.parse_args()

    orchestrator = SetupOrchestrator()

    if args.brew_only:
        orchestrator.run_brew_only()
    elif args.config_only:
        orchestrator.run_config_only()
    elif args.dotfiles_only:
        orchestrator.run_dotfiles_only()
    else:
        orchestrator.run_full_setup()


if __name__ == "__main__":
    main()
