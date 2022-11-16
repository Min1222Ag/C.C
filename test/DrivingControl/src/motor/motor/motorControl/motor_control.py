from time import sleep as sleep 
from motor import motor
from ../../../../../RobotVision/src import interface
import os

class motorControl:
    '''
    Driving using two DC motors
    '''
    def __init__(self, pins): # pins is a list consisting of 6 GPIO pins
        self.right_motor = Motor([pins[0], pins[1]], pins[2], "right") # right motor
        self.left_motor = Motor([pins[3], pins[4]], pins[5], "left") # left motor

    def ahead(self):
        # drive ahead
        self.right_motor.forward()
        self.left_motor.forward()

    def back(self):
        # drive back
        self.right_motor.backward()
        self.left_motor.backward()

    def right(self):
        # drive right
        self.right_motor.backward()
        self.left_motor.forward()

    def left(self):
        # drive left
        self.right_motor.forward()
        self.left_motor.backward()

    def stop(self):
        # stop driving
        self.right_motor.stop()
        self.left_motor.stop()
