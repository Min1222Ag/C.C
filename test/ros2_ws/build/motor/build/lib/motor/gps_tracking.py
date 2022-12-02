# for GPS
import serial

# for magnetometer
import adafruit_bno055
import board

from time import sleep as sleep
from math import sin, cos, asin, sqrt, radians, atan2, degrees

R = 6378.1 # radius of earth

class GPSTracking:
    '''
    Find location itself using GPS
    '''
    def __init__(self):

        # GPS setting
        self.gps = serial.Serial("/dev/ttyUSB0")

        # magnetometer setting
        self.i2c = board.I2C()
        self.magnetometer = adafruit_bno055.BNO055_I2C(self.i2c)

    def getGPSPoints(self, data):
        if "$GPGGA" in data:
            data = data.split(',')[1:]
            latitude = self.convertData(data[1])
            longitude = self.convertData(data[3])
            return latitude, longitude

    def convertData(self, data):
        data = data.split(".")
        degree = int(data[0][:-2])
        min_frac = float(data[0][-2:]+"."+data[1])
        data_res = degree + (min_frac/60)
        return data_res

    def readGPS(self):
        if self.gps.readable():
            data = self.gps.readline().replace(b'\n', b'').replace(b'\r', b'').decode()
            return self.getGPSPoints(data)

    def distance(lat1, lon1, lat2, lon2):

        lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2)

        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1

        distance = 2*R*asin(sqrt(sin(lat_diff/2)**2 + cos(lat1)*cos(lat2)*sin(lon_diff/2)**2))

        return distance

    def bearing(lat1, lon1, lat2, lon2):

        lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2)
        lon_diff = lon2 - lon1

        x = cos(lat2)*sin(lon_diff)
        y = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(lon_diff)

        bearing = atan2(x, y)

        return bearing
