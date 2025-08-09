#!/bin/bash

temp=$(sensors | grep "junction" | awk '{print $2}' | tr -d '+°C')
echo "$temp°C"
