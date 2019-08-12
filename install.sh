#!/bin/sh

sudo pip3 install spidev
sudo pip3 install RPi.GPIO
sudo pip3 install Pillow
sudo pip3 install requests
sudo pip3 install websocket_client

dir=$(pwd)
dir="$dir/python3/main.py"
pwdesc=$(echo $dir | sed 's_/_\\/_g')

echo $pwdesc

sed -e "s/WORKING_DIR/$pwdesc/g" service.template > rbtv_schedule.service

sudo cp rbtv_schedule.service /etc/systemd/user/
sudo systemctl enable rbtv_schedule.service
sudo systemctl start rbtv_schedule.service