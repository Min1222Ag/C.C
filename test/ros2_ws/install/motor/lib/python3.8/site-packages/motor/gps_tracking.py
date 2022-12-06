# for GPS
import serial

# for magnetometer
import adafruit_bno055
import board

import pandas as pd

from time import sleep as sleep
from math import sin, cos, asin, sqrt, radians, atan2, degrees

R = 6378.1 # radius of earth
SUBGOALS_FILE = "home/pi/C.C/test/PathSetting/path_info/on_going.json"

SUBGOALS_FILE = "home/pi/C.C/test/PathSetting/path_info/on_going.json"
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
            if data[1] == '' or data[3] == '':
                return None
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

    def distance(self, lat1, lon1, lat2, lon2):

        lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2)

        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1

        distance = 2*R*asin(sqrt(sin(lat_diff/2)**2 + cos(lat1)*cos(lat2)*sin(lon_diff/2)**2))

        return distance

    def bearing(self, lat1, lon1, lat2, lon2):

        lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2)
        lon_diff = lon2 - lon1

        x = cos(lat2)*sin(lon_diff)
        y = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(lon_diff)

        bearing = atan2(x, y)

        return bearing

    def spheral2cartesian(self, lat, lon):
        x = cos(lat) * cos(lon)
        y = cos(lat) * sin(lon)
        z = sin(lat)
        return x, y, z

    def weighted_mean(self, lat1, lon1, lat2, lon2, n):

        lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2)

        x1, y1, z1 = self.spheral2cartesian(lat1, lon1)
        x2, y2, z2 = self.spheral2cartesian(lat2, lon2)

        x = (1-n)*x1 + n*x2
        y = (1-n)*y1 + n*y2
        z = (1-n)*z1 + n*z2

        lon = atan2(y, x)
        hyp = sqrt(x**2 + y**2)
        lat = atan2(z, hyp)

        return lat, lon

    def subgoals(self, start_lat, start_lon, end_lat, end_lon, gap):
        
        horizontal_meter = self.distance(start_lat, start_lon, start_lat, dest_lon)*1000
        vertical_meter = self.distance(start_lat, start_lon, dest_lat, dest_lon)*1000

        horizontal_n = int(horizontal_meter/gap)
        vertical_n = int(vertical_meter/gap)

        if horizontal_n == 0:
            horizontal_n = 1

        if vertical_n == 0:
            vertical_n = 1

        subgoals_df = pd.DataFrame(columns=['latitude', 'longitude'])

        i = 0
        flip_direction = False

        for v in list(range(1, vertical_n+1)):
            for h in list(range(1, horizontal_n+1)):

                lat_ratio = v/vertical_n
                if flip_direction:
                    lon_ratio = 1 - h/horizontal_n
                else:
                    lon_ratio = h/horizontal_n

                lat = start_lat*lat_ratio + dest_lat*(1-lat_ratio)
                lon = start_lon*lon_ratio + dest_lon*(1-lon_ratio)

                subgoals_df.loc[i] = [lat, lon]
                i += 1

            flip_direction = not flip_direction

        with open(SUBGOALS_FILE, 'w') as f:
            json.dump(subgoals_df, f)
