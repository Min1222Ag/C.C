import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


trig_pin = 26

PIN_TRIGGER_A = 6
PIN_TRIGGER_B = 13
PIN_TRIGGER_C = 19
PIN_TRIGGER_D = 26

PIN_TRIGGER_X = 27

triggers = [PIN_TRIGGER_A, 
            PIN_TRIGGER_B,
            PIN_TRIGGER_C,
            PIN_TRIGGER_D,
            PIN_TRIGGER_X
            ]

PIN_ECHO_A = 10
PIN_ECHO_B = 9
PIN_ECHO_C = 11
PIN_ECHO_D = 5

PIN_ECHO_X = 22

echos = [PIN_ECHO_A, 
        PIN_ECHO_B,
        PIN_ECHO_C,
        PIN_ECHO_D,
        PIN_ECHO_X
        ]

proxs = []
GPIO.setup(echos[0], GPIO.IN)
GPIO.setup(echos[1], GPIO.IN)
GPIO.setup(echos[2], GPIO.IN)
GPIO.setup(echos[3], GPIO.IN)
GPIO.setup(echos[4], GPIO.IN)

GPIO.setup(triggers[0], GPIO.OUT)
GPIO.setup(triggers[1], GPIO.OUT)
GPIO.setup(triggers[2], GPIO.OUT)
GPIO.setup(triggers[3], GPIO.OUT)
GPIO.setup(triggers[4], GPIO.OUT)

while True:
    GPIO.output(triggers[0], GPIO.LOW)
    GPIO.output(triggers[1], GPIO.LOW)
    GPIO.output(triggers[2], GPIO.LOW)
    GPIO.output(triggers[3], GPIO.LOW)
    GPIO.output(triggers[4], GPIO.LOW)
    sleep(1)

    GPIO.output(triggers[0], GPIO.HIGH)
    sleep(0.001)
    GPIO.output(triggers[0], GPIO.LOW)
    
    while(GPIO.input(echos[0]) == 0):
        s1 = time.time()
    while(GPIO.input(echos[0]) == 1):
        e1 = time.time()

    GPIO.output(triggers[1], GPIO.HIGH)
    sleep(0.001)
    GPIO.output(triggers[1], GPIO.LOW)
    while(GPIO.input(echos[1]) == 0):
        s2 = time.time()
    while(GPIO.input(echos[1]) == 1):
        e2 = time.time()
    
    GPIO.output(triggers[2], GPIO.HIGH)
    sleep(0.001)
    GPIO.output(triggers[2], GPIO.LOW)
    while(GPIO.input(echos[2]) == 0):
        s3 = time.time()
    while(GPIO.input(echos[2]) == 1):
        e3 = time.time()

    GPIO.output(triggers[3], GPIO.HIGH)
    sleep(0.001)
    GPIO.output(triggers[3], GPIO.LOW)
    while(GPIO.input(echos[3]) == 0):
        s4 = time.time()
    while(GPIO.input(echos[3]) == 1):
        e4 = time.time()
    
    GPIO.output(triggers[4], GPIO.HIGH)
    sleep(0.001)
    GPIO.output(triggers[4], GPIO.LOW)
    while(GPIO.input(echos[4]) == 0):
        s5 = time.time()
    while(GPIO.input(echos[4]) == 1):
        e5 = time.time()

    d1 = round((e1 - s1)*343200/2, 2)
    d2 = round((e2 - s2)*343200/2, 2)
    d3 = round((e3 - s3)*343200/2, 2)
    d4 = round((e4 - s4)*343200/2, 2)
    d5 = round((e5 - s5)*343200/2, 2)
    print(d1, d2, d3, d4, d5)

GPIO.cleanup()
