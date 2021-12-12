import os
import sys
import time
from gps import *

GPSTime = ''

try:
    gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
except:
    print ("ERROR: No GPS data, exiting. Will try again in 5 minutes.")
    os.system('sudo . /home/pi/Tools/GPSTime/SetTimeFromGPS.sh &')
    sys.exit()

while True:
    report = gpsd.next()

    print ("Waiting for valid GPS data... ")

    if report['class'] == 'TPV':
        GPSTime = getattr(report,'time','')

    if GPSTime != '':
        UTCTime = GPSTime[0:4] + GPSTime[5:7] + GPSTime[8:10] + ' ' + GPSTime[11:19]
        print ("GPS Time in UTC: ", UTCTime)
        os.system('sudo date -u --set="%s"' % UTCTime)
        sys.exit()