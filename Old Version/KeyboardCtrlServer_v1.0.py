#!/usr/bin/python3

# -----------------------------------------------------
# Connect rasp-pi and PC with TCP to control the wheels
# Server end
# Including obstacle avoidance
# Coding: utf-8
# -----------------------------------------------------

# -------- Import necessary packages --------
import socket
from time import sleep
from sys import exit
import RPi.GPIO as GPIO
from WheelCtrl import WheelCtrl

# -------------------- Socket settings --------------------
# Define host ip: Rpi's IP
# HOST_IP = "192.168.3.19"
HOST_IP = "169.254.233.2"
HOST_PORT = 8888
print("Starting socket: TCP...")
# 1. Create socket object: socket = socket.socket(family, type)
socketTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
hostAddr = (HOST_IP, HOST_PORT)
# 2. Bind socket to addr: socket.bind(address)
socketTcp.bind(hostAddr)
# 3. Listen connection request: socket.listen(backlog)
socketTcp.listen(1)
# 4. Wait for client's request: connection, address = socket.accept()
socketCon, (client_ip, client_port) = socketTcp.accept()
print("Connection accepted from %s." %client_ip)
welcMsg = "Welcome to RPi TCP server!"
socketCon.send(welcMsg.encode('utf-8'))

# -------- Infrared obstacle avoidance settings --------
# Set pin numbers
DR = 16         # Right channel signal
DL = 19         # Left channel signal
# Initialize pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

# ------------------------ Main code ------------------------
# Initialization
Wc = WheelCtrl()
print("Receiving commands from PC...")
# Main loop
while True:
    try:
        # Receive 1024 bytes a time
        dataRecv = socketCon.recv(1024)
        if len(dataRecv) > 0:
            print("Received: %s\n" %dataRecv.decode('utf-8'))
            # Deal with exit message
            if dataRecv.decode('utf-8') == 'exit':
                socketTcp.close()
                exit(1)
            # Judge the movement of car
            if dataRecv.decode('utf-8') == 'stop':
                Wc.stop()
            else:
                if dataRecv.decode('utf-8') == 'forward':
                    leftCtrl  =  20
                    rightCtrl =  20
                elif dataRecv.decode('utf-8') == 'backward':
                    leftCtrl  = -20
                    rightCtrl = -20
                elif dataRecv.decode('utf-8') == 'left':
                    leftCtrl  = -20
                    rightCtrl =  20
                elif dataRecv.decode('utf-8') == 'right':
                    leftCtrl  =  20
                    rightCtrl = -20
                Wc.setMotor(leftCtrl, rightCtrl)
            continue
    except Exception:
            socketTcp.close()
            exit(1)