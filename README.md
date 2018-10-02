# Raspberry Pi Zero W Network Real Time Environment Sensing  
Tutorial on using raspberry pi to realize real time temperature & humidity measurement logging to remote ssh host, based on Bash Scripting and Python in command line. 

## About  
Use [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi) (Here uses Pi Zero W for it's light weight, same works for raspberry pi 3 B+) to setup a auto running IoT to collect temperature and humidity data, with highly configurable features, such as logging time interval, remote host sync time interval, auto reboot, auto restart, etc.  

Most of the system functionality is realized by using bash script, while python is used for interfacing with sensor hardware. The main requirement here for the board is that it has to support wifi and I2C communication (usually comes with GPIO).

## Requirement  
**Hardware**  
+ Raspberry Pi 3 model B+ ($35) or Raspberry Pi Zero W ($10)
+ SSH host running on PC or linux server
+ Adafruit Si7021 Temperature and Humidity Sensor ([$7](https://www.adafruit.com/product/3251))

**Software**  
+ Shell Scripting 
+ Python 
+ Crontab 
+ SSH 
+ microSD memory

**Optional**  
+ MicroB OTG hub / header
+ DC power supply 
+ Mini HDMI cable / header 
+ Raspberry Pi case 


## Install 
1. Burn raspbian image using dd  
   The native system [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) may or may not come with the microSD card you bought. Assume you need to burn the Raspbian image onto MicroSD manually by yourself. this step will show how to do it.  For those who don't need a graphical environment or familar with linux, *Raspbian Stretch Lite* is a great choice, while *Raspbian Stretch with Desktop* is also available for those who are more comfortable with desktop environment.   
   To do this on linux, plug in your microSD (might need a microSD to USB reader), find out the corresponding device name using lsblk:  
   
   ```bash
   dd -if /path/to/downloaded/raspbian/image -of /dev/sdx[replace x with real device name -bs 4M -status progress -oflag sync
   ```
   To do this on Window, you may consider [NOOBS](https://www.raspberrypi.org/downloads/noobs/) or [Rufus](http://rufus.akeo.ie/) tool  



More editing in progress...   



2. mount image, copy folder 'config' and file 'sensorlog.py' to /home
3. Boot raspberry pi zero W, set user pi passwd and root passwd, enable ssh
4. Install necessary package using install_package.sh
5. check if timezone is right 
6. setup passwrod free ssh:
   + ssh-keygen to generate ssh key, empty password
   + cat .ssh/ssh_rsa.pub | ssh yulu@internal.raizenlab.ph.utexas.edu 'cat >> .ssh/authorized_keys'
7. enable i2c through raspi-config   
8. In DeviceConfig.txt, change the device name, ssh sync path, run setup_cron.sh to install crontab
9. reboot and check 
