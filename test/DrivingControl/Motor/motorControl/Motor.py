import RPi.GPIO as GPIO
from time import sleep as sleep

GPIO.setwarnings(False)

class Motor:
    def __init__(self, direction_pins, block_pin, label="unlabeled"):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(direction_pins[0], GPIO.OUT)
        GPIO.setup(direction_pins[1], GPIO.OUT)
        GPIO.setup(block_pin, GPIO.OUT)

        GPIO.output(direction_pins[0], GPIO.LOW)
        GPIO.output(direction_pins[1], GPIO.LOW)
        GPIO.output(block_pin, GPIO.LOW)

        self.direction_pins = direction_pins
        self.block_pin = block_pin
        self.label = label

    def forward(self):
        if(GPIO.input(self.direction_pins[0]) and GPIO.input(self.direction_pins[1])):
            if(not GPIO.input(self.block_pin)):
                GPIO.output(self.block_pin, GPIO.HIGH)
            pass
        else:
            while(GPIO.input(self.block_pin)):
                GPIO.output(self.block_pin, GPIO.LOW)
                print("{}: {}pin {}".format(self.label, self.block_pin, GPIO.input(self.block_pin)))
            sleep(0.01)
        
            GPIO.output(self.direction_pins[0], GPIO.HIGH)
            print("{}: {}pin {}".format(self.label, self.direction_pins[0], GPIO.input(self.direction_pins[0])))
            GPIO.output(self.direction_pins[1], GPIO.HIGH)
            print("{}: {}pin {}".format(self.label, self.direction_pins[1], GPIO.input(self.direction_pins[1])))
            sleep(0.01)

            while(not GPIO.input(self.direction_pins[0]) and not GPIO.input(self.direction_pins[1])):
                GPIO.output(self.block_pin, GPIO.LOW)
                print("{}: {}pin {}".format(self.label, self.block_pin, GPIO.input(self.block_pin)))

            GPIO.output(self.block_pin, GPIO.HIGH)
            print("{}: {}pin {}".format(self.label, self.block_pin, GPIO.input(self.block_pin)))

    def backward(self):
        if(GPIO.input(self.direction_pins[0]) and GPIO.input(self.direction_pins[1])):
            while(GPIO.input(self.block_pin)):
                GPIO.output(self.block_pin, GPIO.LOW)
                print("{}: {}pin {}".format(self.label, self.block_pin, GPIO.input(self.block_pin)))
            sleep(0.01)
        
            GPIO.output(self.direction_pins[0], GPIO.LOW)
            print("{}: {}pin {}".format(self.label, self.direction_pins[0], GPIO.input(self.direction_pins[0])))
            GPIO.output(self.direction_pins[1], GPIO.LOW)
            print("{}: {}pin {}".format(self.label, self.direction_pins[1], GPIO.input(self.direction_pins[1])))
            sleep(0.01)

            while(GPIO.input(self.direction_pins[0]) and GPIO.input(self.direction_pins[1])):
                GPIO.output(self.block_pin, GPIO.LOW)
                print("{}: {}pin {}".format(self.label, self.block_pin, GPIO.input(self.block_pin)))

            GPIO.output(self.block_pin, GPIO.HIGH)
            print("{}: {}pin {}".format(self.label, self.block_pin, GPIO.input(self.block_pin)))
        else:
            if(not GPIO.input(self.block_pin)):
                GPIO.output(self.block_pin, GPIO.HIGH)
            pass

    def stop(self):
            GPIO.output(self.block_pin, GPIO.LOW)
