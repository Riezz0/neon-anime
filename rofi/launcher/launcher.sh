#!/usr/bin/env bash

dir="$HOME/.config/rofi/launcher/"
theme='launcher'

## Run
rofi \
    -show drun \
    -theme ${dir}/${theme}.rasi \
