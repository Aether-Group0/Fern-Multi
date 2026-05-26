#!/bin/bash


echo -e "\e[32m"
echo "Ebola Puller"


publicip=$(curl -s https://api.ipify.org)

if [ -z "$publicip" ]; then
    echo "Failed to retrieve public IP."
    read -p "Press enter to exit..."
    exit 1
fi


if command -v tshark >/dev/null 2>&1; then
    tshark_path=$(command -v tshark)
else
    echo "Wireshark/TShark not found."
    echo "Please install it via: sudo apt install tshark"
    read -p "Press enter to exit..."
    exit 1
fi

echo "tshark found! ($tshark_path)"
echo


"$tshark_path" -D
echo


read -p "Interface # or Name: " interface

clear
echo
echo "IP Dump"
echo "-------"
echo


sudo "$tshark_path" -i "$interface" -f "udp" \
    -Y "stun.type == 0x0101 && stun.att.type == 0x0020 && stun.att.ipv4 != $publicip" \
    -T fields -e stun.att.ipv4