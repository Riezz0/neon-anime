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
if ! command -v yay &> /dev/null; then
    echo "yay is not installed."
    install_yay
else
    echo "yay is already installed (version: $(yay --version | head -n 1))."
fi

#-----Sys-Update-----#
echo "Updating The System"
sleep 3
yay -Syyu --noconfirm

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
  python-psutil \
	python-virtualenv \
	python-gobject \
	xfce4-settings \
  xfce-polkit \
	exa \
	rofi-wayland \
  goverlay-git \
  neovim

#-----AUR-Package-Update-----#
echo "Checking For Updates For Newly Installed Packges"
sleep 3
yay -Syyu --noconfirm

#-----Oh-My-Zsh-----#
echo "Installing Oh-My-Zsh"
sleep 3

mkdir -p /home/$USER/dots/omz


git clone "https://github.com/zsh-users/zsh-autosuggestions.git" "/home/$USER/dots/omz/zsh-autosuggestions/"
git clone "https://github.com/zsh-users/zsh-syntax-highlighting.git" "/home/$USER/dots/omz/zsh-syntax-highlighting/"
git clone "https://github.com/zdharma-continuum/fast-syntax-highlighting.git" "/home/$USER/dots/omz/fast-syntax-highlighting/"
git clone --depth 1 -- "https://github.com/marlonrichert/zsh-autocomplete.git" "/home/$USER/dots/omz/zsh-autocomplete/"
git clone "https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv.git" "/home/$USER/dots/omz/autoswitch_virtualenv/"

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

rm -rf ~/.zshrc

cp -r /home/$USER/dots/omz/autoswitch_virtualenv/ ~/.oh-my-zsh/custom/plugins/
cp -r /home/$USER/dots/omz/fast-syntax-highlighting/ ~/.oh-my-zsh/custom/plugins/
cp -r /home/$USER/dots/omz/zsh-autocomplete/ ~/.oh-my-zsh/custom/plugins/
cp -r /home/$USER/dots/omz/zsh-autosuggestions/ ~/.oh-my-zsh/custom/plugins/
cp -r /home/$USER/dots/omz/zsh-syntax-highlighting/ ~/.oh-my-zsh/custom/plugins/

#-----Config-Symlink-----#
echo "Symlinking Configs"
sleep 3

rm -rf /home/$USER/dots/omz/
rm -rf /home/$USER/.config/hypr
rm -rf /home/$USER/.config/kitty
ln -s /home/$USER/dots/.zshrc /home/$USER/
ln -s /home/$USER/dots/fastfetch/ /home/$USER/.config/
ln -s /home/$USER/dots/gtk-3.0/ /home/$USER/.config/
ln -s /home/$USER/dots/gtk-4.0/ /home/$USER/.config/
ln -s /home/$USER/dots/hypr/ /home/$USER/.config/
ln -s /home/$USER/dots/kitty/ /home/$USER/.config/
ln -s /home/$USER/dots/nvim/ /home/$USER/.config/
ln -s /home/$USER/dots/rofi/ /home/$USER/.config/
ln -s /home/$USER/dots/scripts/ /home/$USER/.config/
ln -s /home/$USER/dots/waybar/ /home/$USER/.config/
ln -s /home/$USER/dots/.icons/ /home/$USER/
ln -s /home/$USER/dots/.themes/ /home/$USER/

echo "Symlinking Sys Configs"
sleep 3
sudo rm -rf /usr/share/icons/default
sudo cp -r /home/$USER/dots/sys/cursors/default /usr/share/icons/
sudo cp -r /home/$USER/dots/sys/cursors/Future-black-cursors /usr/share/icons/

sudo mkdir -p /usr/share/bg/
sudo cp -r /home/$USER/dots/hypr/bg/bg.jpg /usr/share/bg/
sudo cp -r /home/$USER/dots/.icons/oomox-anime_room /usr/share/icons/
sudo cp -r /home/$USER/dots/.themes/oomox-anime_room /usr/share/themes/

#-----Apply-Theme-----#
echo "Applying Theme"
Sleep 3

gsettings set org.gnome.desktop.interface cursor-theme "Future-black-cursors"
gsettings set org.gnome.desktop.interface icon-theme "oomox-anime_room"
gsettings set org.gnome.desktop.interface gtk-theme "oomox-anime_room"
gsettings set org.gnome.desktop.interface font-name "Jetbrains Mono Nerd Font 11"
gsettings set org.gnome.desktop.interface document-font-name "Jetbrains Mono Nerd Font 11"
gsettings set org.gnome.desktop.interface monospace-font-name "Jetbrains Mono Nerd Font 11"
gsettings set org.gnome.desktop.wm.preferences titlebar-font "Jetbrains Mono Nerd Font 11"
sudo cp -r /home/$USER/dots/sys/lightdm/ /etc/

wal -i ~/.config/hypr/bg/bg.jpg

echo "Installation Complete !!!"
echo "Rebooting The System"

sleep 3
sudo systemctl reboot



