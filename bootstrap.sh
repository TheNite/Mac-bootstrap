#!/usr/bin/env bash
# Bootstrap Script
# Run this first on a fresh macOS install to set up prerequisites
# Usage: ./bootstrap.sh [--non-interactive]

set -e  # Exit on error

# Parse arguments
NON_INTERACTIVE=false
for arg in "$@"; do
    case $arg in
        --non-interactive|-n)
            NON_INTERACTIVE=true
            shift
            ;;
    esac
done

echo "========================================"
echo "  macOS Setup - Bootstrap"
echo "========================================"
echo ""

if [[ "$NON_INTERACTIVE" == true ]]; then
    echo "Running in non-interactive mode"
    echo ""
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}[ERROR]${NC} This script must be run on macOS"
    exit 1
fi

echo -e "${GREEN}[INFO]${NC} Checking prerequisites..."
echo ""

# Check for Command Line Tools
echo -e "${GREEN}[INFO]${NC} Checking for Command Line Tools..."
if xcode-select -p &>/dev/null; then
    echo -e "${GREEN}[OK]${NC} Command Line Tools already installed"
else
    echo -e "${YELLOW}[INSTALL]${NC} Installing Command Line Tools..."
    echo "NOTE: A dialog will appear. Please click 'Install' and wait for completion."
    xcode-select --install
    echo ""

    if [[ "$NON_INTERACTIVE" == true ]]; then
        # Auto-wait by polling for installation
        echo "Waiting for Command Line Tools installation (checking every 5 seconds)..."
        while ! xcode-select -p &>/dev/null; do
            sleep 5
        done
        echo -e "${GREEN}[OK]${NC} Command Line Tools installed"
    else
        # Interactive mode - wait for user confirmation
        echo "Waiting for Command Line Tools installation to complete..."
        echo "Press Enter after the installation finishes..."
        read -r
    fi
fi
echo ""

# Check for Homebrew
echo -e "${GREEN}[INFO]${NC} Checking for Homebrew..."
if command -v brew &>/dev/null; then
    echo -e "${GREEN}[OK]${NC} Homebrew already installed"
    echo -e "${GREEN}[INFO]${NC} Updating Homebrew..."
    brew update
else
    echo -e "${YELLOW}[INSTALL]${NC} Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == "arm64" ]]; then
        echo -e "${GREEN}[INFO]${NC} Adding Homebrew to PATH (Apple Silicon)..."
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi
echo ""

# Check for Python 3
echo -e "${GREEN}[INFO]${NC} Checking for Python 3..."
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}[OK]${NC} Python ${PYTHON_VERSION} already installed"
else
    echo -e "${YELLOW}[INSTALL]${NC} Installing Python 3 via Homebrew..."
    brew install python
fi
echo ""

# Check for pip
echo -e "${GREEN}[INFO]${NC} Checking for pip..."
if command -v pip3 &>/dev/null; then
    echo -e "${GREEN}[OK]${NC} pip already installed"
else
    echo -e "${YELLOW}[INSTALL]${NC} Installing pip..."
    python3 -m ensurepip --upgrade
fi
echo ""

# Install Python requirements
echo -e "${GREEN}[INFO]${NC} Installing Python dependencies..."
if [[ -f "requirements.txt" ]]; then
    pip3 install -r requirements.txt
    echo -e "${GREEN}[OK]${NC} Python dependencies installed"
else
    echo -e "${YELLOW}[WARNING]${NC} requirements.txt not found, skipping Python dependencies"
fi
echo ""

# Make scripts executable
echo -e "${GREEN}[INFO]${NC} Making scripts executable..."
chmod +x setup.py
if [[ -d "scripts" ]]; then
    chmod +x scripts/*.py
fi
echo -e "${GREEN}[OK]${NC} Scripts are now executable"
echo ""

echo "========================================"
echo -e "${GREEN}[SUCCESS]${NC} Bootstrap complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Edit config.yaml to customize your preferences"
echo "  2. Run: ./setup.py"
echo ""
echo "Optional:"
echo "  - Professional setup only: ./setup.py --brew-only --config-only"
echo "  - Install personal apps: ./scripts/install_personal_apps.py"
echo ""
