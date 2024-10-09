#!/bin/bash
# Installs Avahi and creates discovery service

sudo apt install -y avahi-daemon avahi-utils
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon

sudo cp ./config/filmstore_discovery.service /etc/avahi/services/filmstore_discovery.service

sudo systemctl restart avahi-daemon
