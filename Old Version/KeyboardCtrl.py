#!/usr/bin/python3

# Import necessary libraries
import RPi.GPIO as GPIO
from time import sleep
from WheelCtrl import WheelCtrl
from pynput import keyboard

# Parameter definition
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

# Initialize wheel controller
Wc = WheelCtrl()

# Initialize controling ports
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CTR, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(A, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(B, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(C, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(D, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BUZ, GPIO.OUT)

# When key pressed, move the car
def on_press(key):
    # Judge if a direction key is pressed and response
    if key == keyboard.Key.up or keyboard.Key.down\
        or keyboard.Key.left or keyboard.Key.right:
        if key == keyboard.Key.up:
            leftCtrl  =  20
            rightCtrl =  20
        elif key == keyboard.Key.down:
            leftCtrl  = -20
            rightCtrl = -20
        elif key == keyboard.Key.left:
            leftCtrl  = -20
            rightCtrl =  20
        elif key == keyboard.Key.right:
            leftCtrl  =  20
            rightCtrl = -20
        Wc.setMotor(leftCtrl, rightCtrl)
    else:
        Wc.stop()
    
# When key released, stop the car
def on_release(key):
    # Judge if a direction key is pressed and response
    if key == keyboard.Key.up or keyboard.Key.down\
        or keyboard.Key.left or keyboard.Key.right:
            Wc.stop()
    else:
        Wc.stop()

# Main loop
while True:
    with keyboard.Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()