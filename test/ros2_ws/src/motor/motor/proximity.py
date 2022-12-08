import RPi.GPIO as GPIO
import time
from time import sleep as sleep

GPIO.setwarnings(False)

class Proximity:
    '''
    Sense the distance to object
    '''
    def __init__(self, trigger_pin, echo_pin, label="unlabeled"):

        GPIO.setmode(GPIO.BCM) # BCM mode

        # initialization
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.output(trigger_pin, GPIO.LOW)
        GPIO.setup(echo_pin, GPIO.IN)

        self.trigger_pin = trigger_pin # type: int
        self.echo_pin = echo_pin # type: int
        self.label = label # type: str
    
    def measure(self):
        
        # trigger the sensor
        GPIO.input(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, GPIO.LOW)
        
        # wait for echo pulse
        while GPIO.input(self.echo_pin) == 0:
            s = time.time() # pulse end
        while GPIO.input(self.echo_pin) == 1:
            e = time.time() # pulse end
            return self.calculate_distance(s, e) # return distance

    def calculate_distance(self, start, end):
        # calculating distance using pulse duration
        # distance = speed*time/2
        # speed of sound = 34300 -> time/2 = 17150
        duration = end - start # time
        distance = round(duration*17150, 2) # to two decimal places
        return distance # return distance by the centimeter
