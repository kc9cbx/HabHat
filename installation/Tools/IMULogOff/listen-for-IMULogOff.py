#!/usr/bin/env python

import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(26, GPIO.FALLING)

# Terminate any running instances of PresIMULogger.py
os.system("sudo pkill -f PresIMULogger.py &")
