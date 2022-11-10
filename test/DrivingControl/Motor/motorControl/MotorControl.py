from time import sleep as sleep 
from Motor import Motor

class MotorControl:
    def __init__(self, pins):
        self.right_motor = Motor([pins[0], pins[1]], pins[2], "right")
        self.left_motor = Motor([pins[3], pins[4]], pins[5], "left")

    def ahead(self):
        print("ahead")
        self.right_motor.forward()
        self.left_motor.forward()

    def back(self):
        print("back")
        self.right_motor.backward()
        self.left_motor.backward()

    def right(self):
        print("right")
        self.right_motor.backward()
        self.left_motor.forward()

    def left(self):
        print("left")
        self.right_motor.forward()
        self.left_motor.backward()

    def stop(self):
        print("stop")
        self.right_motor.stop()
        self.left_motor.stop()
