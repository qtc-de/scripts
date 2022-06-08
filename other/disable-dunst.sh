#!/bin/bash

STATUS=$(dunstctl is-paused)

if [[ "$STATUS" = "true" ]]; then
    dunstctl set-paused toggle
    dunstify -t 3000 'Notificatios enabled'

else
    dunstify -t 3000 'Disabling notifications' && sleep 3
    dunstctl set-paused toggle
fi
