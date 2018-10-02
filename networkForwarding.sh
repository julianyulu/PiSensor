#/bin/sh
if [[ `id -u` != 0 ]]; then
    echo "Please run with 'sudo'!"
    echo "sudo $0 $*"
    exit 1;
fi

device=$(ip addr |grep enp | cut -d":" -f2 |tr -d " "| sed -n 2p)
echo "Found raspberry pi interface: *$device*"

wifi=$(ip addr |grep wlp | cut -d: -f2 |tr -d " " | sed -n 1p)
echo "Found wifi interface: *$wifi*"

sysctl net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -o $wifi -j MASQUERADE
iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $device -o $wifi -j ACCEPT
echo "Wifi forwarding established !"



