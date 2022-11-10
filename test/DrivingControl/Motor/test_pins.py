import RPi.GPIO as gpio
from time import sleep as sleep

pins = [23]

gpio.setmode(gpio.BCM)

for pin in pins:
    gpio.setup(pin, gpio.OUT)
    gpio.output(pin, False)

for e, pin in enumerate(pins):
    for i in range(e+3):
        print("{}- {} HIGH".format(pin, i))
        gpio.output(pin, True)
        sleep(1)
        gpio.output(pin, False)
        print("LOW")
        sleep(1)
gpio.output(pins[0], True)
sleep(0.01)

while(gpio.input(pins[0])):
    gpio.output(pins[0], False)

gpio.cleanup()

