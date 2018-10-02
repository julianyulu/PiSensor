#!/bin/sh
thisFilePath="$( cd "$(dirname "$0")" ; pwd -P)"
sudo killall wpa_supplicant
sudo wpa_supplicant -B -i wlan0 -c /home/pi/config/.wpa_conf
sudo dhclient wlan0

