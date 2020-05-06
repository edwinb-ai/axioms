# ==== EXPORTS ==== #
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# fd-fzf exports
export FZF_DEFAULT_COMMAND='fdfind --type file --follow --hidden --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# Add Cargo (Rust package manager) to PATH
# export PATH=$HOME/.cargo/bin:$PATH

# Export Julia binaries
export PATH=$HOME/programs/julia-1.4.1/bin:$PATH

# Add poetry
export PATH=$HOME/.poetry/bin:$PATH

# ==== THEME ==== #
# ZSH_THEME="spaceship"

# Enable the starship prompt
eval "$(starship init zsh)"

# ==== OPTIONS ==== #
# Uncomment the following line to automatically update without prompting.
DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# ==== PLUGINS ==== #
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(z git zsh-syntax-highlighting)

# ==== FILES ==== #
# Load oh-my-zsh
source $ZSH/oh-my-zsh.sh

# Add custom configuration
export STARSHIP_CONFIG=~/.config/starship.toml