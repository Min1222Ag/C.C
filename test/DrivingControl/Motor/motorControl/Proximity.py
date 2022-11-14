import RPi.GPIO as GPIO
import time
from time import sleep as sleep
from threading import Semaphore

GPIO.setwarnings(False)
semaphore = Semaphore(1)

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

        self.running = False # running status
        
        self.trigger_pin = trigger_pin # type: int
        self.echo_pin = echo_pin # type: int
        self.label = label # type: str

    def measure(self):
    # measure distance to object

        semaphore.acquire()
        # triggering
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        sleep(0.00001) # settle
        GPIO.output(self.trigger_pin, GPIO.LOW)

        # waiting echo
        while GPIO.input(self.echo_pin) == 0:
            start = time.time() # pulse start
        while GPIO.input(self.echo_pin) == 1:
            end = time.time() # pulse end
        
        semaphore.release()

        # calculating distance using pulse duration
        # distance = speed*time/2
        # speed of sound = 34300
        duration = end - start # time
        distance = round(duration * 17150, 2) # unit: cm

        return distance

    def keep_measuring(self):
    # constantly measure distance
        self.running = True
        while(self.running):
            distance = self.measure()
            if distance < 3:
                print("{}: {}cm".format(self.label, self.measure()))
