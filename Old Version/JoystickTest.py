#!/usr/bin/python3

# Import necessary libraries
import RPi.GPIO as GPIO
from time import sleep
from WheelCtrl import WheelCtrl

# Parameter definition
Wc = WheelCtrl()
CTR = 7         # Controling signal (use for stop)
A = 8           # Forward
B = 9           # Right
C = 10          # Left
D = 11          # Back
BUZ = 4         # Buzzer controling signal

# Function of buzzer controling
def beepOn():
    GPIO.output(BUZ, GPIO.HIGH)
def beepOff():
    GPIO.output(BUZ, GPIO.LOW)

# Initialize controling ports
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CTR, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(A, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(B, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(C, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(D, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BUZ, GPIO.OUT)

try:
    while True:
        if GPIO.input(CTR) == 0:
            beepOn()
            Wc.stop()
            print("center")
            while GPIO.input(CTR) == 0:
                sleep(0.01)
        elif GPIO.input(A) == 0:
            beepOn()
            Wc.forward()
            print("up")
            while GPIO.input(A) == 0:
                sleep(0.01)
        elif GPIO.input(B) == 0:
            beepOn()
            Wc.right()
            print("right")
            while GPIO.input(B) == 0:
                sleep(0.01)
        elif GPIO.input(C) == 0:
            beepOn()
            Wc.left()
            print("left")
            while GPIO.input(C) == 0:
                sleep(0.01)
        elif GPIO.input(D) == 0:
            beepOn()
            Wc.backward()
            print("down")
            while GPIO.input(D) == 0:
                sleep(0.01)
        else:
            beepOff()
except KeyboardInterrupt:
    GPIO.cleanup()
