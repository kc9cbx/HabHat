#!/bin/bash

sudo raspi-config nonint do_hostname "$1"
sudo hostname -b "$1"
sudo systemctl restart avahi-daemon
