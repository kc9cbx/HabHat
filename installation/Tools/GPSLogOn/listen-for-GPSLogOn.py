#!/usr/bin/env python

import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(6, GPIO.FALLING)

# Start GPS Log
os.system("sudo python3 /home/pi/Tools/Logger/GPSLogger.py &")
