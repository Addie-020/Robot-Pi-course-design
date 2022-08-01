#!/usr/bin/python3


# -----------------------------------------------------
# PC and Robot-pi Interaction
# Server End on Raspberry Pi
# Coding: utf-8
# -----------------------------------------------------


# ------------- Import necessary packages -------------
from threading import Thread
from time import sleep
from sys import exit
import GlobalVar as gv
import WheelCtrl as wc
import TcpServer as ts
import InfObstAvoid as ioa
import ThreadSetting as tds


# --------------------- Main code ---------------------

# Set TCP parameters
HOST_IP = "192.168.3.19"            # Define host ip: Rpi's IP (A209)
# HOST_IP = "169.254.233.2"           # Define host ip: Rpi's IP (Wire)
HOST_PORT = 8888                    # Define host port: Default 8888

# Initialization
gv._init()
wc.wheelInit()
ts.tcpInit(HOST_IP, HOST_PORT)
ioa.avoidInit()
tds.threadInit()

# Create threads
td1 = Thread(target = ts.recvData, args = ())           # TCP receive data
td2 = Thread(target = ioa.obstAvoid, args = ())         # Infrarer obstacle avoidance
# Start threads
td1.start()
td2.start()

# Main loop
while True:
    # Deal with exit message
    exitFlag = gv.getVal("exitFlag")
    if exitFlag:
        sleep(0.5)
        break
    else:
        continue