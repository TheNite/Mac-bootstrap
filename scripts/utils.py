"""
Shared utilities for macOS setup scripts

This module provides common functionality used across all setup scripts
including logging, command execution, and configuration loading.
"""

import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyyaml"], check=True)
    import yaml


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class Logger:
    """Simple logging utility with color support"""

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


def load_config(config_path="config.yaml"):
    """
    Load configuration from YAML file

    Args:
        config_path: Path to config file (relative to project root)

    Returns:
        dict: Configuration dictionary
    """
    # Get project root (parent of scripts directory)
    if Path(__file__).parent.name == 'scripts':
        project_root = Path(__file__).parent.parent
    else:
        project_root = Path(__file__).parent

    config_file = project_root / config_path

    if not config_file.exists():
        Logger.error(f"Config file not found: {config_file}")
        sys.exit(1)

    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def run_command(cmd, check=True, shell=False, capture_output=True):
    """
    Run a shell command with error handling

    Args:
        cmd: Command to run (list or string)
        check: Raise exception on non-zero exit code
        shell: Run command in shell
        capture_output: Capture stdout/stderr

    Returns:
        subprocess.CompletedProcess or None
    """
    try:
        result = subprocess.run(
            cmd,
            check=check,
            shell=shell,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        Logger.error(f"Command failed: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        if e.stderr:
            Logger.error(f"Error: {e.stderr}")
        if check:
            raise
        return None


def command_exists(command):
    """
    Check if a command exists in PATH

    Args:
        command: Command name to check

    Returns:
        bool: True if command exists
    """
    return subprocess.run(
        ["which", command],
        capture_output=True
    ).returncode == 0
