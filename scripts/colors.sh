#!/bin/bash

wal -i /home/$USER/.config/hypr/bg/bg.jpg --cols16
cp -r /home/$USER/.cache/wal/colors-kitty.conf /home/$USER/.config/kitty/colors.conf
cp -r /home/$USER/.cache/wal/colors-hyprland.conf /home/$USER/.config/hypr/colors.conf
cp -r /home/$USER/.cache/wal/colors-waybar.css /home/$USER/.config/waybar/colors.css

pywalfox update
