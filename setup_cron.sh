thisFilePath="$( cd "$(dirname "$0")" ; pwd -P)"

# Parse data file path 
dataPath=`cat $thisFilePath/DeviceConfig.txt | grep DataSavePath | cut -f 2 -d "="`

# Parse sync time parameters
m=`cat $thisFilePath/DeviceConfig.txt | grep SSH_Sync_Minute | cut -f 2 -d "="`
h=`cat $thisFilePath/DeviceConfig.txt | grep SSH_Sync_Hour | cut -f 2 -d "="`
dom=`cat $thisFilePath/DeviceConfig.txt | grep SSH_Sync_Day | cut -f 2 -d "="`
mon=`cat $thisFilePath/DeviceConfig.txt | grep SSH_Sync_Month | cut -f 2 -d "="`
dow=`cat $thisFilePath/DeviceConfig.txt | grep SSH_Sync_DOW | cut -f 2 -d "="`


# Generate config string
echo "@reboot $thisFilePath/setup_wpa.sh" > $thisFilePath/temp.txt
#echo "1 0 * * * $thisFilePath/$thisFilePath/setup_wpa.sh" >> $thisFilePath/temp.txt

echo "@reboot $thisFilePath/sync_host.sh" >> $thisFilePath/temp.txt
echo "$m $h $dom $mon $dow  $thisFilePath/sync_host.sh" >> $thisFilePath/temp.txt

echo "@reboot $dataPath/sensorlog.py" >> $thisFilePath/temp.txt


# Update crontab
cat $thisFilePath/crontab.origin $thisFilePath/temp.txt | crontab -u pi -
rm $thisFilePath/temp.txt

