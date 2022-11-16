import RPi.GPIO as GPIO
import time
from time import sleep as sleep
import threading

lock = threading.Lock()

GPIO.setwarnings(False)

class Proximity(threading.Thread):
    '''
    Sense the distance to object
    '''
    def __init__(self, trigger_pin, echo_pin, label="unlabeled"):
        threading.Thread.__init__(self)

        GPIO.setmode(GPIO.BCM) # BCM mode

        # initialization
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.output(trigger_pin, GPIO.LOW)
        GPIO.setup(echo_pin, GPIO.IN)

        self.trigger_pin = trigger_pin # type: int
        self.echo_pin = echo_pin # type: int
        self.label = label # type: str
        
        self.pulse_start = time.time()
        self.pulse_end = time.time() # pulse end

        self.wait_next = False

        self.start()
    
    def run(self):
        global lock
        print("{} started with trigger {} and echo {}".format(self.label, self.trigger_pin, self.echo_pin))
        while True:

            if self.wait_next:
                continue

            current = GPIO.input(self.trigger_pin)

            if current:
                lock.acquire()
                s = time.time()
                e = s
                while GPIO.input(self.echo_pin) == 0:
                    s = time.time() # pulse end
                while GPIO.input(self.echo_pin) == 1:
                    e = time.time() # pulse end
                print("{} distance: {}".format(self.label, self.measure(s, e)))
                self.wait_next = True
                lock.release()

    def measure(self, start, end):
        # calculating distance using pulse duration
        # distance = speed*time/2
        # speed of sound = 34300
        duration = end - start # time
        distance = round(duration*17150, 2)
        return distance
