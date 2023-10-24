#!/usr/bin/bash
sudo apt-get install python3-usb1 python3-virtualenv vim
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
sudo cp ./pi-config/50-xprinter.rules /etc/udev/rules.d/
cat pi-config/printer.cron | crontab
sudo udevadm control --reload-rules && sudo udevadm trigger
