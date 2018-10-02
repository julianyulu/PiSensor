#!/usr/bin/python3
import time
import os
from datetime import datetime
import board
import busio
import adafruit_si7021


# Read and parse device name and log time intervals from config file
with open('/home/pi/config/DeviceConfig.txt', 'r') as f:
	# Parse device name
	try:
		configStr = f.read()
		deviceConfig = [x for x in configStr.split('\n') if x[:10] == "DeviceName"][0]
		deviceName = deviceConfig[deviceConfig.find('=') + 1 : ].strip()
	except IndexError:
		deviceName = 'unknown' # default device unknow
		pass

	# Parse log time interval
	try:
		logEverySecConfig = [x for x in configStr.split('\n') if x[:11] == "LogEverySec"][0]
		logEverySec = int(logEverySecConfig[logEverySecConfig.find('=') + 1 : ].strip())
		logEverySec = 60 if logEverySec < 1 else logEverySec
	except IndexError:
		logEverySec = 60 #default log every 60 sec

	# Parse  data file path
	try:
		dataSavePathConfig = [x for x in configStr.split('\n') if x[:11] == "DataSavePath"][0]
		dataSavePath = dataSavePathConfig[dataSavePathConfig.find('=') + 1 : ].strip()
	except IndexError:
		dataSavePath = '/home/pi/'

# Initialize I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Establish I2C device
sensor = adafruit_si7021.SI7021(i2c)


# Class for data logging
class  LogTH:
	def __init__(self, every_sec = 60):
		self.every_sec = every_sec

	def _datetime(self):
		return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	def _get_temperature(self):
		return sensor.temperature

	def _get_humidity(self):
		return sensor.relative_humidity

	def logging(self):
		while True:
			filename = os.path.join(dataSavePath,  deviceName + ".".join([datetime.now().strftime("_%Y-%m-%d"), "csv"]))
			if os.path.isfile(filename):
				header = ""
			else:
				header = 'time,temperature,humidity\n'

			with open(filename, "a+") as fout:
				if header:
					fout.write(header)
				fout.write("%s,%.1f,%.1f\n" %(self._datetime(), self._get_temperature(), self._get_humidity()))
			time.sleep(self.every_sec)

if __name__ == '__main__':
	logger = LogTH(logEverySec)
	logger.logging()
