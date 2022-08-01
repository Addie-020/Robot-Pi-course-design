#!/usr/bin/python3


# -----------------------------------------------
# Function: Infrared Obstacle Avoidance settings
# Coding: utf-8
# -----------------------------------------------


# ------------- Import necessary packages -------------
import RPi.GPIO as GPIO
import GlobalVar as gv
import ThreadSetting as tds
import WheelCtrl as wc
import TcpServer as ts


# ------ Create functions for obstacle avoidance ------

# Initialization
def avoidInit(dr=16, dl=19):
    # Set global variable: pin number of sensors
    global DR       # Right channel signal
    global DL       # Left channel signal
    # Initialize global variables
    DR = dr
    DL = dl
    gv.setVal("avoidFlag", 0)
    # Initialize pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

def obstAvoid():
    while True:
        # Deal with exit message
        exitFlag = gv.getVal("exitFlag")
        if exitFlag:
            break
        # Fetch IOA status from GPIO
        drStatus = GPIO.input(DR)
        dlStatus = GPIO.input(DL)
        obstFlag = 0
        obstFlagReg = 0
        # Deal with IOA status
        tds.lockAquire()
        if((dlStatus == 0) or (drStatus == 0)):
            # Stop wheel if met obstacle
            wc.stop()
            obstFlagReg = obstFlag
            obstFlag = 1
        else:
            obstFlagReg = obstFlag
            obstFlag = 0
        gv.setVal("avoidFlag", obstFlag)
        # Send message to PC if obstacle appears or disappears
        if obstFlag != obstFlagReg:
            # Obstacle appears
            if obstFlag:
                str = "obstacle"
            # Obstacle disappears
            else:
                str = "avoided"
            ts.sendData(str)
        tds.lockRelease()