import RPi.GPIO as GPIO
import time
from time import sleep
from threading import Thread
from motorControl.Proximity import Proximity

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
for i, (echo, trigger) in enumerate(zip(echos, triggers)):
    p = Proximity(26, echo, str(i))
    proxs.append(p)

finished_prox = len(proxs)
first = True
while True:

    for prox in proxs:
        if prox.wait_next:
            finished_prox += 1

    if finished_prox != len(proxs):
        finished_prox = 0
        continue

    print("triggered")
    finished_prox = 0
    
    for prox in proxs:
        prox.wait_next = False
    
    GPIO.output(26, GPIO.HIGH)
    sleep(0.001)
    GPIO.output(26, GPIO.LOW)

GPIO.cleanup()
