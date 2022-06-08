#!/bin/bash

# Simple bash script for a xrandr based monitor setup. This script can e.g. run
# by lightdm when configuring it within the /etc/lightdm/lightdm.conf file as
# display-setup-script

SHA256SUM='CHECKSUM  -'
MONITOR_SUM=$(xrandr | grep " connected" | cut -f1 -d" " | sort | sha256sum)

if [ "${SHA256SUM}" = "${MONITOR_SUM}" ]; then
    xrandr --output DP-2   --pos 0x0     --primary
    xrandr --output DP-1-1 --pos 1920x0
    xrandr --output DP-1-2 --pos 3840x0
fi

if [ $UID -eq 1000 ]; then
    nitrogen --restore;
fi
