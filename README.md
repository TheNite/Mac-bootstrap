# Mac-bootstrap

Automated setup tool for configuring a fresh macOS installation with your preferred applications, settings, and configurations.

## Features

- 🚀 **Bootstrap Script**: One-command setup that handles all prerequisites
- 🍺 **Homebrew Package Management**: Automatically install CLI tools and GUI applications
- ✅ **Smart Installation**: Skips already-installed packages for faster re-runs
- 🎨 **Dock Customization**: Clean, minimal dock with only installed apps (using dockutil)
- 📁 **Finder Configuration**: List view, path bar, and status bar enabled
- ⚙️ **System Preferences**: Fast key repeat, trackpad settings, screenshot location, and more
- 🔧 **Git Configuration**: Pre-configured Git settings
- 📝 **YAML Configuration**: Easy-to-edit config file for all preferences
- 🔄 **Version Controlled**: Keep your setup in Git and update from anywhere
- 🧩 **Microservices Architecture**: Independent scripts for each component

## Quick Start

### First-Time Setup (Fresh Mac)

1. **Clone this repository**:
   ```bash
   git clone git@github.com:TheNite/Mac-bootstrap.git
   cd Mac-bootstrap
   ```

2. **Run the bootstrap script** (handles all prerequisites):
   ```bash
   ./bootstrap.sh
   # Or for automated waiting: ./bootstrap.sh --non-interactive
   ```
   This will:
   - Install Command Line Tools (if needed)
   - Install Homebrew (if needed)
   - Install Python 3 (if needed)
   - Install pip and Python requirements
   - Make all scripts executable

3. **Edit configuration** (optional):
   ```bash
   nano config.yaml  # or use any text editor
   ```

4. **Run the full setup**:
   ```bash
   ./setup.py
   ```

### Updating Your Existing Mac

```bash
cd Mac-bootstrap
git pull
./setup.py --config-only  # Apply only system configurations
```

**Note**: The setup automatically skips already-installed packages, making re-runs fast and safe.

## Interactive Steps

### During Bootstrap (bootstrap.sh)

**Interactive Mode** (default):
- Command Line Tools: Opens dialog → Click "Install" → Press Enter when done

**Non-Interactive Mode** (automatic polling):
```bash
./bootstrap.sh --non-interactive
```
- Command Line Tools: Opens dialog → Automatically waits for installation to complete

### During Setup (setup.py)

- **Sudo password**: Required at the start (caches for duration of script)
- **Homebrew installations**: Some may ask for confirmation
- **All package installations**: Automated with skip checks

### After Setup (Manual Steps)

- **NvChad**: First `nvim` run installs plugins interactively
- **1Password**: Manual sign-in required
- **Browsers**: Manual download/install from vendor websites
- **Personal apps**: Run `./scripts/install_personal_apps.py -y` (use `-y` to skip confirmation)

## Configuration

Edit `config.yaml` to customize your setup. Here's what you can configure:

### Homebrew Packages

```yaml
brew_formulae:  # CLI tools
  - git
  - golang
  - python

brew_casks:  # GUI applications
  - iterm2
  - 1password
```

### Dock Settings

```yaml
dock:
  apps:  # Apps in Dock (order matters, Finder is always first)
    - Apps
    - Firefox
    - PyCharm
    - Messages
    - System Settings
    - 1Password
    - Discord
    - iTerm2
    - Sublime Text
  tile_size: 36
  autohide: true
  show_recents: false
```

**How Dock Configuration Works**:
- Uses **dockutil** for reliable Dock management
- Runs **automatically as the last step** of setup.py
- **Only adds apps that are actually installed** on your system
- Skips apps that aren't found with a clear message
- Example: If Firefox isn't installed yet, it will be skipped

**To configure Dock manually** (after installing more apps):
```bash
./scripts/configure_dock.py
```

### Finder Preferences

```yaml
finder:
  default_view: "list"  # icon, list, column, or gallery
  show_path_bar: true
  show_status_bar: true
  show_hidden_files: false
```

### System Preferences

**By default, all system preferences are kept at macOS defaults.**

If you want to customize system settings, uncomment the `system:` section in `config.yaml`:

```yaml
# system:
#   key_repeat_rate: 2  # Faster is lower (1-2 recommended)
#   initial_key_repeat: 15
#   tap_to_click: true
#   tracking_speed: 1.5
#   screenshot_location: "~/Desktop/Screenshots"
```

**Recommendation**: Configure these manually through System Settings to avoid unexpected behavior.

### Git Configuration

```yaml
git:
  default_branch: "main"
  user_name: "Your Name"  # Uncomment and set
  user_email: "your.email@example.com"  # Uncomment and set
```

### Optional Tools

```yaml
optional:
  install_oh_my_zsh: true      # Install Oh My Zsh framework
  install_nvchad: true         # Install NvChad for Neovim
  install_vim_plug: false      # Install Vim-Plug (if you use Vim)
  copy_dotfiles: true          # Copy zsh config files
```

## Usage Options

### Full Setup (Fresh Install)
```bash
./setup.py
```

### Install Only Homebrew Packages
```bash
./setup.py --brew-only
```

### Apply Only System Configurations
```bash
./setup.py --config-only
```

### Copy Only Dotfiles
```bash
./setup.py --dotfiles-only
```

### Run Individual Scripts

Each component can be run independently:

```bash
# Install Homebrew
./scripts/install_homebrew.py

# Install all packages (professional setup)
./scripts/install_packages.py

# Install personal apps (Gaming, utilities, media, network tools - 14 apps total)
./scripts/install_personal_apps.py
# Or skip confirmation: ./scripts/install_personal_apps.py -y

# Configure Dock only
./scripts/configure_dock.py

# Configure Finder only
./scripts/configure_finder.py

# Configure system preferences only
./scripts/configure_system.py

# Configure Git only
./scripts/configure_git.py

# Install Oh My Zsh and plugins only
./scripts/install_zsh.py

# Install NvChad only
./scripts/install_nvchad.py

# Copy dotfiles only
./scripts/copy_dotfiles.py
```

### Professional vs Personal Setup

The setup is designed to keep professional and personal applications separate:

- **Professional setup** (`./setup.py`): Installs development tools, productivity apps, and professional software
- **Personal apps** (`./scripts/install_personal_apps.py`): Installs personal apps including:
  - **Gaming**: Discord, Jagex Launcher, RuneLite, Steam
  - **Cloud Storage**: Google Drive
  - **Utilities**: AppCleaner, Keka, VeraCrypt
  - **Media**: VLC, Handbrake
  - **Remote/Network**: AnyDesk, Cyberduck, Wireshark
  - **System Tools**: balenaEtcher

This separation allows you to:
- Run the main setup on work machines without personal apps
- Easily customize what gets installed in different contexts
- Keep your professional and personal environments distinct

## What Gets Installed

### Default CLI Tools
- **Git** - Version control
- **GitHub CLI (gh)** - GitHub from terminal
- **Go** (latest) - Programming language
- **Node.js** (latest) - JavaScript runtime
- **Python** (latest) - Programming language
- **Terraform** - Infrastructure as Code
- **Neovim** - Modern Vim-based editor
- **1Password CLI** - Password manager CLI
- **dockutil** - Dock management utility
- **ripgrep** - Fast grep alternative
- **fzf** - Fuzzy finder
- **bat** - Better cat with syntax highlighting
- **eza** - Modern ls replacement
- **tmux** - Terminal multiplexer
- **wget** - File downloader
- **jq** - JSON processor

### Fonts
- **JetBrains Mono Nerd Font** - Required for NvChad icons

### Default GUI Applications

**Development:**
- **iTerm2** - Modern terminal emulator
- **Visual Studio Code** - Code editor
- **Sublime Text** - Lightweight text editor
- **JetBrains Toolbox** - JetBrains IDE manager
- **Docker** - Containerization platform
- **Bruno** - Modern API client (Postman alternative)

**Productivity:**
- **1Password** - Password manager

### Development Tools
- **Oh My Zsh** - Zsh framework with plugins (git, docker, kubectl, golang, python, node, npm, brew, fzf, z, copypath)
- **Zsh Custom Plugins**:
  - **zsh-autosuggestions** - Fish-like autosuggestions as you type
  - **zsh-syntax-highlighting** - Real-time syntax highlighting for commands
  - **zsh-interactive-cd** - Interactive directory navigation with fzf
  - **you-should-use** - Reminds you to use existing aliases
  - **zsh-bat** - Enhanced cat command with syntax highlighting
- **NvChad** - Neovim configuration with IDE-like features
- **Custom Zsh configs** - Aliases and functions for productivity

**Note**: Browsers should NEVER be installed via Homebrew. Install manually from vendor websites:
- **Firefox**: https://www.firefox.com/
- **Chrome**: https://www.google.com/chrome/
- **Brave**: https://brave.com/

## Dotfiles & Shell Configuration

The setup includes customized Zsh configuration files:

### `.zshrc`
- Oh My Zsh integration with enhanced plugins:
  - **Built-in**: git, docker, kubectl, golang, python, node, npm, brew, fzf, z, copypath
  - **Custom**: zsh-autosuggestions (fish-like suggestions), zsh-syntax-highlighting (command validation), zsh-interactive-cd (interactive cd with fzf), you-should-use (alias reminders), zsh-bat (cat with syntax)
- Custom PATH configuration
- FZF and 1Password CLI setup

### `.zsh_aliases`
Over 30 useful aliases including:
- Navigation shortcuts (`..`, `...`, `....`)
- Modern replacements (`ll` with eza, `cat` with bat)
- Git shortcuts (`gs`, `ga`, `gc`, `gp`, etc.)
- Development aliases (`py`, `nv`, `vim` → nvim)
- System utilities (`brewup`, `myip`, `cleanup`)

### `.zsh_functions`
Productivity functions including:
- `mkcd` - Create directory and cd into it
- `extract` - Extract any archive type
- `gclone` - Clone repo and cd into it
- `port` / `killport` - Find/kill process on port
- `serve` - Quick HTTP server
- `backup` - Backup file with timestamp
- `opget` - Get password from 1Password
- And many more!

## Manual Steps After Setup

1. **Sign in to 1Password** and sync your passwords
2. **Run Neovim** to complete NvChad setup:
   ```bash
   nvim
   ```
   Wait for plugins to install on first launch.
3. **Configure SSH keys**:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
4. **Set up VS Code Settings Sync** (sign in with GitHub)
5. **Install browsers manually** (NEVER use Homebrew):
   - Firefox: https://www.firefox.com/
   - Chrome: https://www.google.com/chrome/
   - Brave: https://brave.com/
6. **Install personal apps** (optional):
   ```bash
   ./scripts/install_personal_apps.py
   ```
7. **Install PyCharm** via JetBrains Toolbox (already installed)
8. **Re-run Dock configuration** if you install more apps later:
   ```bash
   ./scripts/configure_dock.py
   ```
   Note: Dock is already configured by the main setup with all currently-installed apps.
9. **Restart your Mac** for all changes to take effect
10. **Open iTerm2** and set JetBrains Mono Nerd Font as the default font

## Keeping Your Setup Updated

### Push Changes to GitHub

```bash
git add config.yaml
git commit -m "Update macOS setup configuration"
git push
```

### Pull Changes on New Mac

```bash
git pull
./setup.py
```

## Architecture

This setup uses a **microservices-style architecture** where each component is handled by a dedicated script:

- **Modularity**: Each script handles one specific responsibility
- **Independence**: Scripts can be run individually or as a full setup
- **Maintainability**: Easy to update, debug, and extend specific components
- **Reusability**: Common utilities shared via `utils.py` module

## Project Structure

```
Mac-bootstrap/
├── bootstrap.sh                  # Bootstrap script (run this first!)
├── setup.py                      # Main orchestrator script
├── config.yaml                   # Configuration file
├── requirements.txt              # Python dependencies (PyYAML)
├── README.md                     # Documentation
├── .gitignore                   # Git ignore rules
├── scripts/                     # Microservice-style scripts
│   ├── utils.py                 # Shared utilities (logging, config loading)
│   ├── install_homebrew.py      # Homebrew installation
│   ├── install_packages.py      # Professional packages (with skip checks)
│   ├── install_personal_apps.py # Personal apps (with skip checks)
│   ├── configure_dock.py        # Dock configuration (using dockutil)
│   ├── configure_finder.py      # Finder preferences
│   ├── configure_system.py      # System preferences
│   ├── configure_git.py         # Git configuration
│   ├── install_zsh.py           # Oh My Zsh and plugins
│   ├── install_nvchad.py        # NvChad for Neovim
│   └── copy_dotfiles.py         # Dotfiles deployment
└── dotfiles/                    # Dotfiles directory
    ├── .zshrc                   # Zsh configuration
    ├── .zsh_aliases             # Zsh aliases
    └── .zsh_functions           # Zsh functions
```

## Troubleshooting

### "Permission denied" error
Make sure the script is executable:
```bash
chmod +x setup.py
```

### Homebrew installation fails
Install Homebrew manually first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Dock doesn't update
Restart the Dock manually:
```bash
killall Dock
```

### System preferences don't apply
Some changes require a restart:
```bash
sudo shutdown -r now
```

## Customization Tips

### Add More Homebrew Packages

Search for packages:
```bash
brew search <package-name>
```

Then add to `config.yaml`:
```yaml
brew_formulae:
  - your-package

brew_casks:
  - your-app
```

### Keep Personal Overrides Private

Create a `config.local.yaml` (ignored by Git) with your personal settings like Git username/email.

## License

MIT License - Feel free to fork and customize!

## Contributing

This is a personal setup tool, but feel free to fork it and adapt it to your needs!

## Credits

Created to automate macOS fresh installs and keep configuration version controlled.
