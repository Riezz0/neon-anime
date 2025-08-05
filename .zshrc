# Startup Commands
#fastfetch --kitty-direct /home/$USER/.config/fastfetch/ArchLinux.png --logo-width 22 --logo-height 10 --logo-padding-top 5 --logo-padding-left 2

fastfetch

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"



# Theme
ZSH_THEME="robbyrussell"

# Plugins
plugins=(git zsh-autosuggestions zsh-syntax-highlighting fast-syntax-highlighting zsh-autocomplete autoswitch_virtualenv $plugins)

# Import
source $ZSH/oh-my-zsh.sh

# aliases
alias v="nvim"
alias ls="exa -lag --icons"
