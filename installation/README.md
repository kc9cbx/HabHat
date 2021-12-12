# Installation
### OS
The bellow steps were tested on Raspberry Pi OS Lite, based on "buster". However, most of the functionality is rather basic, so it should work on other versions of Raspberry Pi OS, Desktop or Lite. As for the compute hardware, it was tested on Raspberry Pi Zero W and Raspberry Pi 4B+

### Step-By-Step Instructions
1. Start with creating an SD card with Raspberry Pi OS, following the instructions [here](https://www.raspberrypi.org/software/). Once that process is complete, leave the card in your computer, as we need to do a few more things before you try to boot from it.
2. Download the zip of this repo and extract it somewhere on your computer. Wherever you unzipped it, you will find two folders: boot and Tools.
	- Take the entire Tools folder and copy it to the root of the boot partition of the SD card. This folder has all the logging code along with utility scripts and config files that will make setting everything up much easier. 
	- Then, open the boot folder and edit the wpa_supplicant.conf file, by entering your WiFi SSID and password. Save the file and copy it (just the file, not the folder) to the root of the SD card boot partition.
	 - Lastly, copy the SSH file from the boot folder directly to root of the SD card boot partition. This will enable SSH server on your Pi. This is an optional step that is particularly handy if you are planning on running the Pi headless.
3. With all of this on your SD card, remove it from your computer, put it in your Pi and power it up. If your Pi is connected to a display you should be able to log in with default credentials. As soon as you log in, use the [raspi-config tool](https://www.raspberrypi.org/documentation/computers/configuration.html#the-raspi-config-tool) to rename your Raspberry Pi to something unique and change the default password.
4. First, lets update the OS, remove any extraneous packages, and clean up the temp files:
```
sudo apt update
sudo apt -y upgrade
sudo apt -y autoremove
sudo apt clean
```
5. Next, lets configure I2C and serial interfaces:
```
sudo raspi-config nonint do_i2c 0
sudo sh -c "echo 'force_turbo=1' >> /boot/config.txt"
sudo sh -c "echo 'enable_uart=1' >> /boot/config.txt"
sudo sh -c "echo 'pi3-disable-bt' >> /boot/config.txt"
sudo sh -c "echo 'dtparam=i2c_arm=on' >> /boot/config.txt"
sudo sh -c "echo 'dtparam=i2c1=on' >> /boot/config.txt"
sudo sed -e s/console=serial0,115200//g -i /boot/cmdline.txt
sudo systemctl disable hciuart
```
6. Copy over the Tools folder. This is a very important step, as many subsequent steps expect this folder to be in a specific location. Don't use sudo for this command:
```
cp -r /boot/Tools /home/pi/Tools
```
7. Install a separate service for each of the buttons. Buttons are not required, just convenient. If you are not using them, you can safely skip this step:

```
# Set up the Power Off button, register as service and start the service
cd /home/pi/Tools/PowerOff
sudo cp listen-for-shutdown.py /usr/local/bin/
sudo chmod +x /usr/local/bin/listen-for-shutdown.py
sudo cp listen-for-shutdown.sh /etc/init.d/
sudo chmod +x /etc/init.d/listen-for-shutdown.sh
sudo update-rc.d listen-for-shutdown.sh defaults
sudo /etc/init.d/listen-for-shutdown.sh start

# Set up the GPS Off button, register as service and start the service
cd /home/pi/Tools/GPSLogOff
sudo cp listen-for-GPSLogOff.py /usr/local/bin/
sudo chmod +x /usr/local/bin/listen-for-GPSLogOff.py
sudo cp listen-for-GPSLogOff.sh /etc/init.d/
sudo chmod +x /etc/init.d/listen-for-GPSLogOff.sh
sudo update-rc.d listen-for-GPSLogOff.sh defaults
sudo /etc/init.d/listen-for-GPSLogOff.sh start

# Set up the GPS On button, register as service and start the service
cd /home/pi/Tools/GPSLogOn
sudo cp listen-for-GPSLogOn.py /usr/local/bin/
sudo chmod +x /usr/local/bin/listen-for-GPSLogOn.py
sudo cp listen-for-GPSLogOn.sh /etc/init.d/
sudo chmod +x /etc/init.d/listen-for-GPSLogOn.sh
sudo update-rc.d listen-for-GPSLogOn.sh defaults
sudo /etc/init.d/listen-for-GPSLogOn.sh start

# Set up the IMU Off button, register as service and start the service
cd /home/pi/Tools/IMULogOff
sudo cp listen-for-IMULogOff.py /usr/local/bin/
sudo chmod +x /usr/local/bin/listen-for-IMULogOff.py
sudo cp listen-for-IMULogOff.sh /etc/init.d/
sudo chmod +x /etc/init.d/listen-for-IMULogOff.sh
sudo update-rc.d listen-for-IMULogOff.sh defaults
sudo /etc/init.d/listen-for-IMULogOff.sh start

# Set up the IMU On button, register as service and start the service
cd /home/pi/Tools/IMULogOn
sudo cp listen-for-IMULogOn.py /usr/local/bin/
sudo chmod +x /usr/local/bin/listen-for-IMULogOn.py
sudo cp listen-for-IMULogOn.sh /etc/init.d/
sudo chmod +x /etc/init.d/listen-for-IMULogOn.sh
sudo update-rc.d listen-for-IMULogOn.sh defaults
sudo /etc/init.d/listen-for-IMULogOn.sh start
```
8. Reboot:
```
sudo reboot
```
9. When the Pi powers back up, let's install basic packages and some troubleshooting tools/utilites:
```
sudo apt -y install build-essential wiringpi gpsd gpsd-clients i2c-tools screen inotify-tools
```
10. Then, let's install Python 3 and necessary modules:
```
sudo apt -y install python3-dev python3-pip python3-numpy python3-smbus
sudo pip3 install RPi.GPIO pyserial fraction easydict gps mpu9250-jmdev smbus2
```

11. Copy over GPSd configuration file that tells the service where to find the GPS receiver. In this case it is the UART on the Pi's GPIO:
```
sudo cp /home/pi/Tools/GPSdConfig/gpsd /etc/default/gpsd
```

12. Add GPSd service to the "dialout" group to give it access to the serial port and the GPS connected to it:
```
sudo cp /home/pi/Tools/GPSdConfig/gpsd /etc/default/gpsd
```
13. Finally, copy over the auto start configuration. This ensures that logging will start automatically at power up, ensure that system time is set from the GPS time, and initialize the LEDs.
```
sudo cp /home/pi/Tools/Autostart/rc.local /etc/rc.local
```
14. Reboot!
```
sudo reboot
```
15. Place the HabHat GPS receiver in the clear view of the sky. If everything worked as expected, once you pi boots, 20-30 seconds later you will see your IMU log LED turn on. Once your GPS acquires a lock, GPS log LED will also light up. At this point, you are ready to fly!



