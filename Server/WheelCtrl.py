#!/usr/bin/python3


# ---------------------------------------
# Function: Wheel Controling Settings
# Coding: utf-8
# ---------------------------------------


# ------------- Import necessary packages -------------
import RPi.GPIO as GPIO
from time import sleep
from sys import exit
import GlobalVar as gv


# ------- Create functions for wheel controling -------

# Initialize wheel controling settings
def wheelInit(ain1=12, ain2=13, ena=6, bin1=20, bin2=21, enb=26):
    # Define global variables
    global AIN1         # Controling signal 1 of left wheel
    global AIN2         # Controling signal 2 of left wheel
    global BIN1         # Controling signal 1 of right wheel
    global BIN2         # Controling signal 2 of right wheel
    global ENA          # Enable signal of left wheel
    global ENB          # Enable signal of right wheel
    global PA           # PWM duty of left wheel
    global PB           # PWM duty of right wheels
    global PWMA
    global PWMB
    # Set initial values of global variables
    AIN1 = ain1
    AIN2 = ain2
    BIN1 = bin1
    BIN2 = bin2
    ENA  = ena
    ENB  = enb
    PA   = 20
    PB   = 20
    # Initialize controling ports
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(AIN1, GPIO.OUT)
    GPIO.setup(AIN2, GPIO.OUT)
    GPIO.setup(BIN1, GPIO.OUT)
    GPIO.setup(BIN2, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    PWMA = GPIO.PWM(ENA, 500)
    PWMB = GPIO.PWM(ENB, 500)
    PWMA.start(PA)
    PWMB.start(PB)
    stop()

# ** Function for direction controling **
#           AIN1 AIN2 BIN1 BIN2
# Forward    0    1    0    1
# Back       1    0    1    0
# Left       1    0    0    1
# Right      0    1    1    0
# Stop       0    0    0    0
def forward():
    PWMA.ChangeDutyCycle(PA)
    PWMB.ChangeDutyCycle(PB)
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
def backward():
    PWMA.ChangeDutyCycle(PA)
    PWMB.ChangeDutyCycle(PB)
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
def left():
    PWMA.ChangeDutyCycle(30)
    PWMB.ChangeDutyCycle(30)
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
def right():
    PWMA.ChangeDutyCycle(30)
    PWMB.ChangeDutyCycle(30)
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
def stop():
    PWMA.ChangeDutyCycle(0)
    PWMB.ChangeDutyCycle(0)
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    
# Function for speed controling
# Left wheel
def setPWMA(value):
    PA = value
    PWMA.ChangeDutyCycle(PA)
# Right wheel
def setPWMB(value):
    PB = value
    PWMB.ChangeDutyCycle(PB)

# Motor function: combine all movement together
# 0 <= left <= 100: left wheel forward
# -100 <= left < 0: left wheel backward
# 0 <= right <= 100: right wheel forward
# -100 <= right < 0: right wheel backward
def setMotor(left, right):
    if((left >= 0) and (left <= 100)):
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        PWMA.ChangeDutyCycle(left)
    elif((left < 0) and (left >= -100)):
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        PWMA.ChangeDutyCycle(0 - left)
    if((right >= 0) and (right <= 100)):
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        PWMB.ChangeDutyCycle(right)
    elif((right < 0) and (right >= -100)):
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
        PWMB.ChangeDutyCycle(0 - right)

# Control the car according to command
def moveCtrl(cmd):
    # Deal with wheel controling event
    if cmd:
        # Stop
        if cmd == 'stop':
            stop()
        # Set direction parameters
        else:
            if cmd == 'forward':
                leftCtrl  =  20
                rightCtrl =  20
            elif cmd == 'backward':
                leftCtrl  = -20
                rightCtrl = -20
            elif cmd == 'left':
                leftCtrl  = -20
                rightCtrl =  20
            elif cmd == 'right':
                leftCtrl  =  20
                rightCtrl = -20
            # Control wheel pins according to direction parameters
            setMotor(leftCtrl, rightCtrl)
            sleep(0.1)
            stop()
    else:
        print("Invalid moving command!")
        exit(1)