# -----------------------------------------------------
# Connect rasp-pi and PC with TCP to control the wheels
# Client end (Rasp-Pi)
# Coding: utf-8wwsswwwas
# -----------------------------------------------------


# ------------- Import necessary packages -------------
import socket
from time import sleep
from sys import exit
from pynput import keyboard


# -------- Keyboard event function definition --------

# Define keyboard event function
# When key pressed, move the car
def on_press(key):
    # Judge if a direction key is pressed and response
    if key == keyboard.KeyCode.from_char('w') or keyboard.KeyCode.from_char('s')\
        or keyboard.KeyCode.from_char('a') or keyboard.KeyCode.from_char('d')\
        or keyboard.Key.space or keyboard.Key.esc:
        if key == keyboard.KeyCode.from_char('w'):
            strSend = "forward"
        elif key == keyboard.KeyCode.from_char('s'):
            strSend = "backward"
        elif key == keyboard.KeyCode.from_char('a'):
            strSend = "left"
        elif key == keyboard.KeyCode.from_char('d'):
            strSend = "right"
        elif key == keyboard.Key.space:
            strSend = "stop"
        elif key == keyboard.Key.esc:
            strSend = "exit"
            listener.stop()
            socketTcp.send(strSend.encode('utf-8'))
            socketTcp.close()
            print("Service closed.\n")
            exit(1)
    # Send corresponding message to Pi
    socketTcp.send(strSend.encode('utf-8'))

# When key released, stop the car
def on_release(key):
    # Judge if a direction key is pressed and response
    if key == keyboard.KeyCode.from_char('w') or keyboard.KeyCode.from_char('s')\
        or keyboard.KeyCode.from_char('a') or keyboard.KeyCode.from_char('d'):
            strSend = "stop"
    socketTcp.send(strSend.encode('utf-8'))


# ---------------------- Main code ----------------------

# Socket settings
SERVER_IP = "192.168.3.19"      # Server's IP: RPi's IP (A209)
# SERVER_IP = "169.254.233.2"    # Server's IP: RPi's IP (Wire)
SERVER_PORT = 8888              # Server's port
# 1. Create socket object: socket = socket.socket(family, type)
print("Starting socket: TCP...\r\n")
serverAddr = (SERVER_IP, SERVER_PORT)
socketTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2. Connect to server: socket.connect(address)
while True:
    try:
        print("Connecting to server @ %s:%d...\r\n" %(SERVER_IP, SERVER_PORT))
        socketTcp.connect(serverAddr)
        break
    except Exception:
        print("Can't connect to server, try it later!\r\n")
        sleep(1)
        continue
print("Use keyboard to control the car...\r\n")

# Main loop
while True:
    try:
        # Listen to keyboard event
        listener = keyboard.Listener(on_press = on_press, on_release = on_release)
        listener.start()
        # Receive 1024 bytes a time
        dataRecv = socketTcp.recv(1024)
        if len(dataRecv) > 0:
            print("Received: %s" %dataRecv.decode('utf-8'))
    except Exception:
        print('error!')
        socketTcp.close()
        socketTcp = None
        exit(1)