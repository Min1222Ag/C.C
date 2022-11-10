#import serial
#import adafruit_bno055
from MotorControl import MotorControl

motorControl = MotorControl([18, 23, 24, 16, 20, 21])
x = ''
#uart = serial.Serial("/dev/serial0")
#sensor = adafruit_bno055.BNO055_UART(uart)

while(x != 'x'):
    x = input()
#    print(sensor)
    if (x == 'a'):
        motorControl.ahead()
    elif (x == 'b'):
        motorControl.back()
    elif (x == 'r'):
        motorControl.right()
    elif (x == 'l'):
        motorControl.left()
    elif (x == 's'):
        motorControl.stop()
