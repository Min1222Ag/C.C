import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

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


for trig, echo in zip(triggers, echos):
    print(trig, echo)
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trig, GPIO.LOW)
    
time.sleep(2)

#calculating distance
for trig, echo in zip(triggers, echos):
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    while GPIO.input(echo) == 0:
        pulse_start_time = time.time()
    while GPIO.input(echo) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print("Distance {}cm".format(distance))

GPIO.cleanup()
