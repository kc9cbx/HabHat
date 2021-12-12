#!/usr/bin/env python

import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(5, GPIO.FALLING)

os.system("poweroff &")