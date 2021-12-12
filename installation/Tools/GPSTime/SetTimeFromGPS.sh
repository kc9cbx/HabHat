#!/bin/bash

# wait for 5 min, giving gps enough time to get a lock
sleep 5m

# Run set time python script
sudo python3 /home/pi/Tools/GPSTime/SetTimeFromGPS.py &

exit 0
