from collections import deque

import adafruit_bno055
import board
from MotorControl import MotorControl

def angle_scope(n):
    if n < 0:
        return 0
    elif n > 359:
        return 359
    else:
        return int(n)

motorControl = MotorControl([18, 23, 24, 16, 20, 21])
sensor = adafruit_bno055.BNO055_I2C(board.I2C())

angle_actions = deque(['ahead']*5 + ['stop']*170 + ['back']*10 + ['stop']*170 + ['ahead']*5)
initial_angle = angle_scope(sensor.euler[0])
angle_actions.rotate(initial_angle)

while(True):
    try:
        angle = angle_scope(sensor.euler[0])
        print(angle)
        eval('motorControl.'+angle_actions[angle])()
    except:
        pass

