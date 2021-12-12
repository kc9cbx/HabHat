#!/bin/bash

# Configure LED GPIOs
# GPS log status LED GPIO
sudo echo "9" > /sys/class/gpio/export
sleep 2
# Set GPIO 9 as output
sudo echo "out" > /sys/class/gpio/gpio9/direction
# Set GPIO 9 to off (0)
sudo echo "0" > /sys/class/gpio/gpio9/value

# IMU log status LED GPIO
sudo echo "11" > /sys/class/gpio/export
sleep 2
# Set GPIO 11 as output
sudo echo "out" > /sys/class/gpio/gpio11/direction
# Set GPIO 11 to off (0)
sudo echo "0" > /sys/class/gpio/gpio11/value

exit 0