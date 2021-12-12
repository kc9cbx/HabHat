import os
import sys
import time
import smbus

from datetime import datetime

from MS5611 import MS5611

from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

# Configure pressure sensor
sensor = MS5611(1)
sensor.setElevationFt(604)
sensor.read()
sensor.printResults()

# Configure IMU
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1,
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu.configure()

# Delay start by 15 seconds
time.sleep(15)

os.system("sudo echo 1 > /sys/class/gpio/gpio11/value &")

# Write Headers to the log file
file = open('/home/pi/PresIMULog.csv', 'a')
file.write("\n\n\n" + "CurrTimestamp" + "," + "pressTempF" + "," + "pressTempC" + "," + "pressAdj" + "," + "pressRaw" + "," + "imuAccel X" + "," + "imuAccel Y" + "," + "imuAccel Z" + "," + "imuGyro X" + "," + "imuGyro Y" + "," + "imuGyro Z" + "," + "imuMag X" + "," + "imuMag Y" + "," + "imuMag Z" + "," + "imuTempC" + "\n")
file.close

while True:
# Get timestamp
    CurrTimestamp = datetime.now()

# Get pressure sensor readings
    pressTempF = sensor.getTempF()
    pressTempC = sensor.getTempC()
    pressAdj = sensor.getPressureAdj()
    pressRaw = sensor.getPressure()

# Get MPU sensor readings
    imuAccel = mpu.readAccelerometerMaster()
    imuGyro = mpu.readGyroscopeMaster()
    imuMag = mpu.readMagnetometerMaster()
    imuTempC = mpu.readTemperatureMaster()

# DEBUG - Print all the results
    print("Timestamp: ", CurrTimestamp)
    print ()
    print ("Temperature: ", round(pressTempF, 2), "F")
    print ("Temperature: ", round(pressTempC, 2), "C")
    print ("Pressure Adjusted: ", round(pressAdj, 2), "hPa")
    print ("Pressure Absolute: ", round(pressRaw, 2), "hPa")
    print ()
    print("Accelerometer", imuAccel)
    print("Gyroscope", imuGyro)
    print("Magnetometer", imuMag)
    print("Temperature", imuTempC)
    print ("\n\n\n")

# Write data to a log
    file = open('/home/pi/PresIMULog.csv', 'a')
    file.write(str(CurrTimestamp) + "," + str(pressTempF) + "," + str(pressTempC) + "," + str(pressAdj) + "," + str(pressRaw) + "," + str(imuAccel[0]) + "," + str(imuAccel[1]) + "," + str(imuAccel[2]) + "," + str(imuGyro[0]) + "," + str(imuGyro[1]) + "," + str(imuGyro[2]) + "," + str(imuMag[0]) + "," + str(imuMag[1]) + "," + str(imuMag[2]) + "," + str(imuTempC) + "\n")
    file.close

#Wait 1/10th of a second before next reading
    time.sleep(0.15)

