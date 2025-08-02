#!/bin/bash

#-----Yay-----#
install_yay() {
    echo "Installing Yay..."
    sleep 3
    sudo pacman -S --needed git base-devel --noconfirm || { echo "Failed to install dependencies"; exit 1; }
    git clone https://aur.archlinux.org/yay.git /tmp/yay || { echo "Failed to clone yay"; exit 1; }
    cd /tmp/yay || exit 1
    makepkg -si --noconfirm || { echo "Failed to build/install yay"; exit 1; }
    cd ..
    rm -rf /tmp/yay
    echo "yay installed successfully!"
}

# Check if yay is installed
if ! command -v yay &> /dev/null; then
    echo "yay is not installed."
    install_yay
else
    echo "yay is already installed (version: $(yay --version | head -n 1))."
fi

#-----AUR-----#

echo "Installing AUR Packages"
sleep 3

yay -S --needed --noconfirm \
	hyprpaper \
	hyprshot \
	hypridle \
	hyprlock \
	hyprpicker \
  swaync \
	wl-clipboard \
	firefox \
  chromium \
	nemo \
	nwg-look \
	python-pywal16 \
	python-pywalfox \
	zsh \
	ttf-jetbrains-mono-nerd \
	ttf-font-awesome \
	ttf-font-awesome-4 \
	ttf-font-awesome-5 \
	waybar \
	rust \
	cargo \
	fastfetch \
	cmatrix \
	pavucontrol \
	waybar-module-pacman-updates-git \
	python-pip \
	python-virtualenv \
	python-gobject \
	xfce4-settings \
	exa \
	rofi-wayland \
  goverlay-git
