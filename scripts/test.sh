#!/bin/bash

# Get GPU stats for AMD RX 6750 XT (no radeontop/rocm-smi)
get_gpu_stats() {
    # 1. GPU Load (from sysfs)
    GPU_LOAD=$(cat /sys/class/drm/card0/device/gpu_busy_percent 2>/dev/null || echo "N/A")
    [[ "$GPU_LOAD" != "N/A" ]] && GPU_LOAD="$GPU_LOAD%"

    # 2. VRAM Usage (from sysfs)
    VRAM_TOTAL=$(cat /sys/class/drm/card0/device/mem_info_vram_total 2>/dev/null | awk '{printf "%.1f GB", $1/1024/1024/1024}')
    VRAM_USED=$(cat /sys/class/drm/card0/device/mem_info_vram_used 2>/dev/null | awk '{printf "%.1f GB", $1/1024/1024/1024}')
    VRAM_USAGE="${VRAM_USED:-N/A} / ${VRAM_TOTAL:-N/A}"

    # 3. Temperature (via sensors)
    TEMP=$(sensors | grep -A 2 "amdgpu" | grep "edge" | awk '{print $2}' || echo "N/A")

    # 4. Core Clock (from sysfs)
    CORE_CLK=$(cat /sys/class/drm/card0/device/pp_dpm_sclk 2>/dev/null | grep "*" | awk '{print $2}' | sed 's/Mhz//')
    CORE_CLK="${CORE_CLK:-N/A} MHz"

    echo -e "GPU Load: $GPU_LOAD\nVRAM: $VRAM_USAGE\nTemp: $TEMP\nCore Clock: $CORE_CLK"
}

# Display in Yad
yad --title="AMD RX 6750 XT Stats" \
    --text="$(get_gpu_stats)" \
    --width=300 \
    --height=200 \
    --button="Close" \
    --text-align=left
