import serial

ser = serial.Serial('/dev/ttyUSB0')

def readGPS():
    while(ser.readable()):
        x = ser.readline().replace(b'\n',b'').replace(b'\r',b'').decode()
        parseGPS(x)
        
def parseGPS(data):
    if "$GPGGA" in data:
        data = data.split(',')[1:]
        print(data)
        run(data)

def timeGPS(time_data):
    time_hour = time_data[:2]
    time_min = time_data[2:4]
    time_sec = time_data[4:6]

    time_data = "Time: {}H {}M {}S".format(time_hour, time_min, time_sec)
    print(time_data)

def latitudeGPS(latitude, hemisphere):
    latitude = latitude.split(".")
    degree = int(latitude[0][:-2])
    min_frac = float(latitude[0][-2:]+"."+latitude[1])
    latitude_res = str(degree + (min_frac/60))
    print("Latitude: {}({})".format(latitude_res, hemisphere))

def longitudeGPS(longitude, hemisphere):    
    longitude = longitude.split(".")
    degree = int(longitude[0][:-2])
    min_frac = float(longitude[0][-2:]+"."+longitude[1])
    longitude_res = str(degree + (min_frac/60))
    print("Longitude: {}({})".format(longitude_res, hemisphere))

def fixGPS(num):
    num = int(num)
    
    fixgps_data = "FixGPS: "
    
    if num == 0:
        fixgps_data += "Invalid"
    elif num == 1:
        fixgps_data += "GPS"
    elif num == 2:
        fixgps_data += "DGPS"
    print(fixgps_data)

def cntSatellite(num):
    print("Satellite number: {}".format(num))

def HDOP(accuracy):
    print("HDOP(Horizontal Dilution of Precision): {}".format(accuracy))

def altitudeGPS(altitude, units):
    print("Altitude: {}{}".format(altitude, units))

def heightGPS(height, units):
    print("Height of geoid above WGS84 ellipsoid: {}{}".format(height, units))

def updateGPS(date):
    print("Last DGPS update: {}".format(date))

def checksumGPS(check):
    print("Checksum: {}".format(check))

def run(data):
    #time
    timeGPS(data[0])
    #latitude
    latitudeGPS(data[1], data[2])
    #longitude
    longitudeGPS(data[3], data[4])
    #fixGPS
    fixGPS(data[5])
    #satellite num
    cntSatellite(data[6])
    #HDOP
    HDOP(data[7])
    #altitude
    altitudeGPS(data[8], data[9])
    #height
    heightGPS(data[10], data[11])
    #update
    updateGPS(data[12])
    #checksum
    checksumGPS(data[13])
    print("----------------------------------------------------------------")

readGPS()

