#!/usr/bin/env python

import os
import subprocess
import sys

sys.path.insert(0, '/home/pi/Tools/Config')
import GONetConfig as cfg

print("Hostname to set: ", cfg.HostName)

os.system("sudo raspi-config nonint do_hostname " + cfg.HostName)
os.system("sudo hostname -b " + cfg.HostName)
os.system("sudo systemctl restart avahi-daemon")
