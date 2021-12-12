import time
import os

fail_count = 0

# Wait 30 sec after launch to start checking file
time.sleep(30) 

# Get initial file size 
file_info = os.stat('/home/pi/PresIMULog.csv')
curr_file_size = file_info.st_size

while True:
# give it a second, then check file size
    time.sleep(1)
    file_info = os.stat('/home/pi/PresIMULog.csv')
    file_size = file_info.st_size

# If file got larger, reset fail count, if not, count a faliure
    if file_size > curr_file_size:
        fail_count = 0
    else:
        fail_count = fail_count + 1

# If we have more than 3 faliures in the row (~3 sec no file size increase) turn off LED
    if fail_count > 3:
        os.system("sudo echo 0 > /sys/class/gpio/gpio11/value &")

# Update current file size
    curr_file_size = file_size