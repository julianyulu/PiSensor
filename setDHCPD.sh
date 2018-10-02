#/bin/sh
if [[ `id -u` != 0 ]]; then
    echo "Please run with 'sudo'!"
    echo "sudo $0 $*"
    exit 1;
fi

dhcpd_config="./dhcpd.conf-rpi"
dhcpd_lease="./leases.db"

#device=$(ip addr |grep enp | cut -d":" -f2 |tr -d " "| sed -n 2p)
device=$1
echo "Found raspberry pi device: *$device*"

echo "Bring *$device* interface up..."
ip link set $device up

echo "Assigning *$device* ip address..."
ip addr add 192.168.7.150/24 dev $device

echo "Running dhcpd on *$device*..."
dhcpd -f -cf $dhcpd_config -lf $dhcpd_lease $device

