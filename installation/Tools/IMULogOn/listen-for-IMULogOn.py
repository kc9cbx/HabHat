#!/usr/bin/env python

import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(19, GPIO.FALLING)

# Start IMU Log
os.system("sudo python3 /home/pi/Tools/Logger/PresIMULogger.py &")
