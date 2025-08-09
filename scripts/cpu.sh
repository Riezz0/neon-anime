#!/bin/bash

temp=$(sensors | grep "Tccd1" | awk '{print $2}' | tr -d '+°C')
echo "$temp°C"
