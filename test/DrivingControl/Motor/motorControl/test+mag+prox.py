from collections import deque
from threading import Thread

import adafruit_bno055
import board
from MotorControl import MotorControl
from Proximity import Proximity

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

proximities = [Proximity(6, 10, 'A'),
            Proximity(13, 9, 'B'),
            Proximity(19, 11, 'C'),
            Proximity(26, 5, 'D'),
            Proximity(27, 22, 'X')]

threads = []
for proximity in proximities:
    thread = Thread(target=proximity.keep_measuring)
    threads.append(thread)
    thread.start()

while(True):
    try:
        angle = angle_scope(sensor.euler[0])
        #print(angle)
        #eval('motorControl.'+angle_actions[angle])()
    except:
        pass

