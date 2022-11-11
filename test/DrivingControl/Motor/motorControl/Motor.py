import RPi.GPIO as GPIO
from time import sleep as sleep

GPIO.setwarnings(False)

class Motor:
    '''
    Control one DC Motor for 3 status; 1) forward spinning; 2) backward spinning; 3) stop
    '''
    def __init__(self, direction_pins, block_pin, label="unlabeled"):
        GPIO.setmode(GPIO.BCM) # BCM mode

        GPIO.setup(direction_pins[0], GPIO.OUT) # pin connected with relay 1: battery's (+) to motor's (+) normally
        GPIO.setup(direction_pins[1], GPIO.OUT) # pin connected with relay 2: battery's (-) to motor's (-) normally
        GPIO.setup(block_pin, GPIO.OUT) # pin connected with relay 3: battery is not connected normally

        # initialize
        GPIO.output(direction_pins[0], GPIO.LOW) # battery's (+) to motor's (+)
        GPIO.output(direction_pins[1], GPIO.LOW) # battery's (-) to motor's (-)
        GPIO.output(block_pin, GPIO.LOW) # unconnect battery

        self.direction_pins = direction_pins # type: list
        self.block_pin = block_pin # type: int
        self.label = label # type: str

    def forward(self):
    # spin forward
        if(GPIO.input(self.direction_pins[0]) and GPIO.input(self.direction_pins[1])): # already doing
            if(not GPIO.input(self.block_pin)):
                GPIO.output(self.block_pin, GPIO.HIGH) # connect battery
            pass

        else:
            while(GPIO.input(self.block_pin)):
                GPIO.output(self.block_pin, GPIO.LOW) # unconnect battery
            sleep(0.01) # settle
        
            GPIO.output(self.direction_pins[0], GPIO.HIGH) # battery's (+) to motor's (+)
            GPIO.output(self.direction_pins[1], GPIO.HIGH) # battery's (-) to motor's (-)
            sleep(0.01) # settle

            while(not GPIO.input(self.direction_pins[0]) and not GPIO.input(self.direction_pins[1])): # multiple check
                GPIO.output(self.direction_pins[0], GPIO.HIGH)
                GPIO.output(self.direction_pins[1], GPIO.HIGH)

            GPIO.output(self.block_pin, GPIO.HIGH) # connect battery

    def backward(self):
    # spin backward
        if(GPIO.input(self.direction_pins[0]) and GPIO.input(self.direction_pins[1])):
            while(GPIO.input(self.block_pin)):
                GPIO.output(self.block_pin, GPIO.LOW) # unconnect battery
            sleep(0.01) # settle
        
            GPIO.output(self.direction_pins[0], GPIO.LOW) # battery's (-) to motor's (+)
            GPIO.output(self.direction_pins[1], GPIO.LOW) # battery's (+) to motor's (-)
            sleep(0.01) # settle

            while(GPIO.input(self.direction_pins[0]) and GPIO.input(self.direction_pins[1])): # multiple check
                GPIO.output(self.direction_pins[0], GPIO.LOW)
                GPIO.output(self.direction_pins[1], GPIO.LOW)

            GPIO.output(self.block_pin, GPIO.HIGH) # connect battery

        else: # already doing
            if(not GPIO.input(self.block_pin)):
                GPIO.output(self.block_pin, GPIO.HIGH) # connect battery
            pass

    def stop(self):
    # stop spinning by unconnecting battery
            GPIO.output(self.block_pin, GPIO.LOW) # unconnect battery
