#!/usr/bin/env python3
"""
Git Configuration Script

Configures Git global settings
"""

import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import Logger, load_config


def configure_git():
    """Configure Git"""
    config = load_config()
    Logger.info("Configuring Git...")

    git_config = config.get('git', {})

    try:
        if 'default_branch' in git_config:
            subprocess.run(
                ['git', 'config', '--global', 'init.defaultBranch', git_config['default_branch']],
                check=True
            )

        if 'user_name' in git_config:
            subprocess.run(
                ['git', 'config', '--global', 'user.name', git_config['user_name']],
                check=True
            )

        if 'user_email' in git_config:
            subprocess.run(
                ['git', 'config', '--global', 'user.email', git_config['user_email']],
                check=True
            )

        Logger.success("Git configured")
        return True

    except Exception as e:
        Logger.error(f"Failed to configure Git: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("  Git Configuration")
    print("=" * 60)
    print()

    if not configure_git():
        sys.exit(1)


if __name__ == "__main__":
    main()
