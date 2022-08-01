# -----------------------------------------------------
# PC and Robot-pi Interaction
# Client End on PC
# Coding: utf-8
# -----------------------------------------------------


# ------------- Import necessary packages -------------
from threading import Thread
from time import sleep
from sys import exit
from pynput import keyboard
import GlobalVar as gv
import TcpClient as tc
import ThreadSetting as tds
import KeyboardCtrl as kc


# --------------------- Main code ---------------------

# Set TCP parameters
SERVER_IP = "192.168.3.19"      # Server's IP: RPi's IP (A209)
# SERVER_IP = "169.254.233.2"    # Server's IP: RPi's IP (Wire)
SERVER_PORT = 8888              # Server's port

# Initialization
gv._init()
gv.setVal("exitFlag", 0)
tc.tcpInit(SERVER_IP, SERVER_PORT)
tds.threadInit()

# Create threads
td1 = Thread(target = tc.recvData, args = ())                                       # TCP receive data
listener = keyboard.Listener(on_press = kc.keyPress, on_release = kc.keyRelease)    # Keyboard event listening
# Start threads
td1.start()
listener.start()

# Main loop
while True:
    # Deal with exit message
    exitFlag = gv.getVal("exitFlag")
    if exitFlag:
        listener.stop()
        sleep(1)
        break
    else:
        continue