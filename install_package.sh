#!/bin/sh
if ping -q -c 1 -W 1 8.8.8.8 > /dev/null;then
    echo "IPv4 up!" > /dev/null
else
    echo "IPv4 down, bringing up!"
    ./setup_wpa.sh
fi

sudo apt-get update
sudo apt-get install ntpdate
sudo apt-get install -y python-smbus i2c-tools python3-pip
sudo pip3 install RPI.GPIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-si7021


sudo cp timezone /etc/timezone
sudo rm /etc/localtime
sudo ln -s /usr/share/zoneinfo/US/Central /etc/localtime
sudo ntpdate pool.ntp.org
