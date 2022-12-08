from time import sleep as sleep
import dc_motor

class motorControl:
    '''
    Driving using two DC motors and control broom motor
    '''
    def __init__(self, pins): # pins is a list consisting of 6 GPIO pins
        self.right_motor = dc_motor.motor(pins[2], [pins[0], pins[1]], "right") # right motor
        self.left_motor = dc_motor.motor(pins[5], [pins[3], pins[4]], "left") # left motor
        self.broom = dc_motor.motor(pins[6], label="broom") # broom motor

    def broom_run(self):
        # broom run
        self.broom.forward()

    def broom_stop(self):
        # broom stop
        self.broom.stop()

    def ahead(self):
        # drive ahead
        print("motor ahead")
        self.right_motor.forward()
        self.left_motor.forward()

    def back(self):
        # drive back
        print("motor back")
        self.right_motor.backward()
        self.left_motor.backward()

    def right_ahead(self):
        self.right()
        sleep(0.5)
        self.ahead()
        sleep(0.5)
    
    def left_ahead(self):
        self.left()
        sleep(0.5)
        self.ahead()
        sleep(0.5)


    def right(self):
        # drive right
        print("motor right")
        self.right_motor.backward()
        self.left_motor.forward()

    def left(self):
        # drive left
        print("motor left")
        self.right_motor.forward()
        self.left_motor.backward()

    def stop(self):
        # stop driving
        print("motor stop")
        self.right_motor.stop()
        self.left_motor.stop()
