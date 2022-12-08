# for GPS
import serial

# for magnetometer
import adafruit_bno055
import board

import pandas as pd

from time import sleep as sleep
from math import sin, cos, asin, sqrt, radians, atan2, degrees

R = 6378.1 # radius of earth
SUBGOALS_FILE = "home/pi/C.C/test/PathSetting/path_info/on_going.json" # where to save generated subgoals information

class GPSTracking:
    '''
    Find location itself using GPS and calculate path-related values
    '''
    def __init__(self):

        self.gps = serial.Serial("/dev/ttyUSB0") # GPS setting with serial communication

        # magnetometer setting with i2c serial communication
        self.i2c = board.I2C()
        self.magnetometer = adafruit_bno055.BNO055_I2C(self.i2c)

    def getGPSPoints(self, data):
        # get the robot's location via GPS sensor
        
        if "$GPGGA" in data: # take only in data format in GPGGA
            data = data.split(',')[1:] # split data in str type based on comma
            if data[1] == '' or data[3] == '': # if there's no data
                return None # return nothing
            latitude = self.convert_data(data[1]) # latitude in float type
            longitude = self.convert_data(data[3]) # longitude in float type
            return latitude, longitude # return a GPS coordinate
    
    def convert_data(self, data):
        # convert str type data to float type data
        
        data = data.split(".") # split based on dot
        degree = int(data[0][:-2]) # left of dot to integer
        min_frac = float(data[0][-2:]+"."+data[1]) # right of dot to floating point number
        data_res = degree + (min_frac/60) # combine two fragments
        return data_res # return float type data

    def readGPS(self):
        # read data using GPS sensor through serial communication
        
        if self.gps.readable(): # if serial is available
            data = self.gps.readline().replace(b'\n', b'').replace(b'\r', b'').decode() # read data from serial
            return self.getGPSPoints(data) # return data

    def distance(self, lat1, lon1, lat2, lon2):
        # calculate distance between two GPS coordinates
        
        lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2) # convert to radian

        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1

        # formula
        # a = sin²(ΔlatDifference/2) + cos(lat1)*cos(lat2)*sin²(ΔlonDifference/2)
        # c = 2*arctan(√(1-a)/√a)
        # distance = R*c where R is the radius of the Earth
        distance = 2*R*asin(sqrt(sin(lat_diff/2)**2 + cos(lat1)*cos(lat2)*sin(lon_diff/2)**2))

        return distance # return distance by the kilometer

    def bearing(self, lat1, lon1, lat2, lon2):
        # calculate bearing between two GPS coordinates

        lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2) # convert to radian
        
        lon_diff = lon2 - lon1

        # formula
        # X = cos lat2 * sin ∆latDifference
        # Y = cos lat1 * sin lat2 – sin lat1 * cos lat2 * cos ∆lonDifference
        # bearing = arctan(Y/X)
        x = cos(lat2)*sin(lon_diff)
        y = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(lon_diff)
        bearing = degrees(atan2(x, y)) # convert radian to degree

        return bearing # return bearing by the degrees

    def intermediate(self, lat1, lon1, lat2, lon2, f):
        # intermediate points on a gread circle GPS coordinate between two coordinates
        d = self.distance(lat1, lat2, lon1, lon2)
        lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2) # convert to radian

        A = sin((1-f)*d)/sin(d)
        B = sin(f*d)/sin(d)
        # convert to cartesian
        x = A*cos(lat1)*cos(lon1) + B*cos(lat2)*cor(lon2)
        y = A*cos(lat1)*sin(lon1) + B*cos(lat2)*sin(lon2)
        z = A*sin(lat1)

        # convert to spheral
        lat = atan2(z, sqrt(x**2+y**2))
        lon = atan2(y, x)

        return lat, lon # return weighted mean

    def subgoals(self, start_lat, start_lon, end_lat, end_lon, gap):
        # generate coordinates of subgoals at an equal given intervals in a rectangular area whose two non-adjacent corners are given two GPS coordinates and save as a file 
        
        # longitude distance, as if the latitude was 0 by the meter
        horizontal_meter = self.distance(start_lat, start_lon, start_lat, dest_lon)*1000
        
        # latitude distance, as if the longitude was 0 by the meter
        vertical_meter = self.distance(start_lat, start_lon, dest_lat, dest_lon)*1000

        # preventing division-by-zero
        if gap <= 0:
            gap = 1

        horizontal_n = int(horizontal_meter/gap) # how many subgoals in horizontal direction
        vertical_n = int(vertical_meter/gap) # how many subgoals in vertical direction

        # preventing division-by-zero
        if horizontal_n == 0:
            horizontal_n = 1
        if vertical_n == 0:
            vertical_n = 1

        subgoals_df = pd.DataFrame(columns=['latitude', 'longitude']) # create new dataframe

        i = 0 # counter for index of dataframe
        flip_direction = False # alternate backward and forward

        for v in list(range(vertical_n+1)): # vertical gap adjusting
            for h in list(range(horizontal_n+1)): # horizontal gap adjusting

                lat_ratio = v/vertical_n # vertical weight of start point
                
                # horizontal weight of start point depending of the direction
                if flip_direction:
                    lon_ratio = 1 - h/horizontal_n
                else:
                    lon_ratio = h/horizontal_n

                # weighted mean as a subgoal
                lat = start_lat*lat_ratio + dest_lat*(1-lat_ratio)
                lon = start_lon*lon_ratio + dest_lon*(1-lon_ratio)

                subgoals_df.loc[i] = [lat, lon] # add to dataframe
                i += 1 # increase counter

            flip_direction = not flip_direction # once the horizontal part ended, change the direction

        # save the result as a file
        with open(SUBGOALS_FILE, 'w') as f:
            json.dump(subgoals_df, f)
