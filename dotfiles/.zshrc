# Path to your oh-my-zsh installation
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="robbyrussell"

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
plugins=(
    git
    docker
    kubectl
    golang
    python
    node
    npm
    brew
    fzf
    z
    copypath
    zsh-autosuggestions
    zsh-syntax-highlighting
    zsh-interactive-cd
    you-should-use
    zsh-bat
)

# Load Oh My Zsh
source $ZSH/oh-my-zsh.sh

# ============================================================================
# User Configuration
# ============================================================================

# Preferred editor
export EDITOR='nvim'
export VISUAL='nvim'

# Language environment
export LANG=en_US.UTF-8

# ============================================================================
# PATH Configuration
# ============================================================================

# Add Go bin to PATH
export GOPATH="$HOME/go"
export PATH="$GOPATH/bin:$PATH"

# Add Python user bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# Add Homebrew to PATH (Apple Silicon)
if [[ -f "/opt/homebrew/bin/brew" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# ============================================================================
# FZF Configuration
# ============================================================================

# Use fd instead of find for fzf
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'

# ============================================================================
# 1Password CLI Configuration
# ============================================================================

# Enable 1Password CLI plugins
if command -v op &> /dev/null; then
    # Set up command-line completion
    eval "$(op completion zsh)"; compdef _op op
fi

# ============================================================================
# Source Custom Configuration Files
# ============================================================================

# Source zsh aliases
[ -f ~/.zsh_aliases ] && source ~/.zsh_aliases

# Source zsh functions
[ -f ~/.zsh_functions ] && source ~/.zsh_functions
