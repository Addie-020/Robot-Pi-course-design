# -----------------------------------------------
# Function: Process Keyboard Events
# Coding: utf-8
# -----------------------------------------------


# ------------- Import necessary packages -------------
from time import sleep
from sys import exit
from turtle import left
from pynput import keyboard
import GlobalVar as gv
import TcpClient as tc
import ThreadSetting as tds


# -------- Keyboard event function definition -------- 

# Define keyboard event function
# When key pressed, move the car
def keyPress(key):
    # Deal with movement locked event
    forwardLock = gv.getVal("forwardLock")
    tds.lockAquire()
    # Judge if a direction key is pressed and response
    if key == keyboard.KeyCode.from_char('w') or keyboard.KeyCode.from_char('s')\
        or keyboard.KeyCode.from_char('a') or keyboard.KeyCode.from_char('d')\
        or keyboard.Key.space:
        if key == keyboard.KeyCode.from_char('w'):
            if forwardLock:
                print("Cannot moving forward!\r\n")
                return
            else:
                strSend = "forward"
        elif key == keyboard.KeyCode.from_char('s'):
            strSend = "backward"
        elif key == keyboard.KeyCode.from_char('a'):
            strSend = "left"
        elif key == keyboard.KeyCode.from_char('d'):
            strSend = "right"
        elif key == keyboard.Key.space:
            strSend = "stop"
    elif key == keyboard.Key.up or keyboard.Key.down\
        or keyboard.Key.left or keyboard.Key.right:
        if key == keyboard.Key.up:
            strSend = "up"
        elif key == keyboard.Key.down:
            strSend = "down"
        elif key == keyboard.Key.left:
            strSend = "left"
        elif key == keyboard.Key.right:
            strSend = "right"
    elif key == keyboard.Key.esc:
        strSend = "exit"
        gv.setVal("exitFlag", 1)
    # Send corresponding message to Pi
    tc.sendData(strSend)
    tds.lockRelease()

# When key released, stop the car
def keyRelease(key):
    # Judge if a direction key is pressed and response
    if key == keyboard.KeyCode.from_char('w') or keyboard.KeyCode.from_char('s')\
        or keyboard.KeyCode.from_char('a') or keyboard.KeyCode.from_char('d'):
            strSend = "stop"
    # Send corresponding message to Pi
    tc.sendData(strSend)