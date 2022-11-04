import RPi.GPIO as gpio
from time import sleep as sleep

pins = [27, ]

gpio.setmode(gpio.BCM)

for pin in pins:
    gpio.setup(pin, gpio.OUT)
    gpio.output(pin, gpio.LOW)

for pin in pins:
    gpio.output(pin, gpio.HIGH)
    sleep(1)
    gpio.output(pin, gpio.LOW)

gpio.cleanup()
