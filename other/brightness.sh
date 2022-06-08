#!/bin/bash

# Adjust the screen brightness. When called without any arguments, the script
# just outputs the current brightness configuration. When invoked with arguments,
# the first argument is interpreted as the desired brightness ratio and the
# screen brightness is adjusted accordingly.

MAX_BRIGHTNESS=$(cat /sys/class/backlight/intel_backlight/max_brightness)

if [ $# -eq 0 ]; then
    ACTUAL_BRIGHTNESS=$(cat /sys/class/backlight/intel_backlight/actual_brightness)
    RATIO=$(( ${ACTUAL_BRIGHTNESS} * 100 / ${MAX_BRIGHTNESS} ))

    echo "[+] Ratio brightness: ${RATIO}"
    echo "[+] Actual brightness: ${ACTUAL_BRIGHTNESS}"
    echo "[+] Maximum brightness: ${MAX_BRIGHTNESS}"

    exit 1

elif [ ${UID} -ne 0 ]; then
    echo "[-] Setting brightness is only allowed as root!"
    exit 1

else
    RE='^[0-9]+$'

    if ! [[ ${1} =~ ${RE} ]] || [[ $1 -gt 100 ]] || [[ $1 -lt 0 ]] ; then
        echo "$0 [<RATIO>]"
        exit 1
        
    elif ! [[ ${MAX_BRIGHTNESS} =~ ${RE} ]]; then
        echo "[-] Internal error!"
        exit 1
    fi

    NEW_VALUE=$(( ${1} * ${MAX_BRIGHTNESS} / 100 ))
    echo ${NEW_VALUE} > /sys/class/backlight/intel_backlight/brightness
fi
