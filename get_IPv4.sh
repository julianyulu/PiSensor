#!/bin/sh
thisFilePath="$( cd "$(dirname "$0")" ; pwd -P)"
device=`cat $thisFilePath/DeviceConfig.txt|grep DeviceName|cut -f 2 -d '='`
dataPath=`cat $thisFilePath/DeviceConfig.txt|grep DataSavePath|cut -f 2 -d '='`

if ping -q -c 1 -W 1 8.8.8.8 > /dev/null;then
	ipv4=`ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}'`
else
	echo "ipv4 down!"
	ipv4="ipv4 down!"
fi
echo $ipv4 > $dataPath/${device}_ip.txt

