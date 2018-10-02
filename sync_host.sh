thisFilePath="$( cd "$(dirname "$0")" ; pwd -P)"

device=`cat $thisFilePath/DeviceConfig.txt|grep DeviceName|cut -f 2 -d '='`
dataPath=`cat $thisFilePath/DeviceConfig.txt|grep DataSavePath|cut -f 2 -d '='`

sshHost=`cat $thisFilePath/DeviceConfig.txt|grep SSHHost|cut -f 2 -d '='`
sshSyncPath=`cat $thisFilePath/DeviceConfig.txt|grep SSHSyncPath|cut -f 2 -d '='`

tzone=`date +%z`
today=`date +%F`
dataFile="$dataPath/${device}_$today.csv"
ipFile="$dataPath/${device}_ip.txt"


if ping -q -c 1 -W 1 8.8.8.8 > /dev/null;then
	echo "IPV4 is up" >/dev/null
else
	echo "IPV4 is down, brining up..."
	$thisFilePath/setup_wpa.sh
fi

if [ $tzone='-0500' ]
then
	if [ -e $dataFile ]
	then
		# Make sure host path exist
		ssh $sshHost "mkdir -p $sshSyncPath"
		rsync $dataFile $ipFile $sshHost:$sshSyncPath
	fi
fi
