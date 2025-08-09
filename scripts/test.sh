#!/bin/bash

# Get AMD GPU stats
get_stats() {
    # Temperature
    temp=$(sensors | grep -m1 "edge" | awk '{print $2}' | tr -d '+°C')
    
    # GPU Usage (sysfs)
    usage=$(cat /sys/class/drm/card0/device/gpu_busy_percent 2>/dev/null || echo "N/A")
    
    # VRAM Usage (sysfs)
    vram_used=$(awk '{print $1/1048576}' /sys/class/drm/card0/device/mem_info_vram_used 2>/dev/null)
    vram_total=$(awk '{print $1/1048576}' /sys/class/drm/card0/device/mem_info_vram_total 2>/dev/null)
    
    # Fan Speed
    fan=$(sensors | grep -m1 "fan" | awk '{print $2}')
    
    # Clock Speed
    clock=$(cat /sys/class/drm/card0/device/pp_dpm_sclk 2>/dev/null | grep "*" | cut -d':' -f2 | cut -d' ' -f2)
    
    # Format output
    echo -en "\0message\x1f<b>AMD GPU Stats</b>\n"
    echo "  Temperature: $temp°C"
    echo "  GPU Usage: $usage%"
    echo "  VRAM: ${vram_used:-N/A}/${vram_total:-N/A} GiB"
    echo "  Fan: ${fan:-N/A} RPM"
    echo "龍 Clock: ${clock:-N/A} MHz"
}

# Display in Rofi
get_stats | rofi -dmenu -p "GPU" -theme-str '
* {
    font: "Fira Code 12";
    text-color: #f8f8f2;
}
window {
    background-color: #282a36;
    border-radius: 8px;
}
listview {
    lines: 5;
    fixed-height: true;
}
message {
    margin: 8px;
    padding: 8px;
    border-bottom: 1px solid #44475a;
}'
