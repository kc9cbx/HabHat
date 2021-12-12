import os
import sys
import time
import smbus
import subprocess

from datetime import datetime

from gps import *

# Delay start by 15 seconds
time.sleep(15)

os.system("sudo echo 1 > /sys/class/gpio/gpio9/value &")

# Write Headers to the log file
file = open('/home/pi/GPSLog.csv', 'a')
file.write("\n\n\n" + "CurrTimestamp" + "," + "GPSLat" + "," + "GPSLong" + "," + "GPSTime" + "," + "GPSAlt" + "," + "GPSSpeed" + "," + "GPSClimb" + "," + "GPSHeading" + "," + "LatErr" + "," + "LonErr" + "," + "SpeerErr" + "," + "HeadErr" + "," + "ClimbErr" + "\n")
file.close

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

while True:

    GPSLat = "0.0"
    GPSLong = "0.0"
    GPSTime = "00:00:00"
    GPSAlt = "000"
    GPSSpeed = "0.00"
    GPSClimb = "0.00"
    GPSHeading = "0.00"
    LatErr = "0.00"
    LonErr = "0.00"
    SpeerErr = "0.00"
    HeadErr = "0.00"
    ClimbErr = "0.00"

# Get timestamp
    CurrTimestamp = datetime.now()
    report = gpsd.next()

    if report['class'] == 'TPV':
        GPSLat = getattr(report,'lat',0.0)
        GPSLong = getattr(report,'lon',0.0)
        GPSTime = getattr(report,'time','')
        GPSAlt = getattr(report,'alt','nan')
        GPSSpeed = getattr(report,'speed','nan')
        GPSClimb = getattr(report,'climb','nan')
        GPSHeading = getattr(report,'track','nan')
        LatErr = getattr(report,'epy','nan')
        LonErr = getattr(report,'epx','nan')
        SpeerErr = getattr(report,'eps','nan')
        HeadErr = getattr(report,'epd','nan')
        ClimbErr = getattr(report,'epc','nan')

# Check for valid data
    if GPSLat != "0.0" and GPSLong != "0.0" and GPSAlt != "nan":
    # DEBUG - Print all the results
        print("Timestamp: ", CurrTimestamp)
        print ("Lat: ", GPSLat)
        print ("Long: ", GPSLong)
        print ("GPS Time: ", GPSTime)
        print ("Altitude: ", GPSAlt)
        print ("Speed: ", GPSSpeed)
        print ("Climb: ", GPSClimb)
        print ("Heading: ", GPSHeading)
        print ("Lat Error: ", LatErr)
        print ("Long Error: ", LonErr)
        print ("Speed Error: ", SpeerErr)
        print ("Heading Error: ", HeadErr)
        print ("Climb Error: ", ClimbErr)
        print ()

    # Get LED Status
        cmd = "cat /sys/class/gpio/gpio9/value"
        state = subprocess.check_output(cmd, shell=True)
        state = state.decode('ASCII')
        state = state.strip()
        if state == "0":
            os.system("sudo echo 1 > /sys/class/gpio/gpio9/value &")

    # Write data to a log
        file = open('/home/pi/GPSLog.csv', 'a')
        file.write(str(CurrTimestamp) + "," + str(GPSLat) + "," + str(GPSLong) + "," + str(GPSTime) + "," + str(GPSAlt) + "," + str(GPSSpeed) + "," + str(GPSClimb) + "," + str(GPSHeading) + "," + str(LatErr) + "," + str(LonErr) + "," + str(SpeerErr) + "," + str(HeadErr) + "," + str(ClimbErr) + "\n")
        file.close

    time.sleep(0.8)

