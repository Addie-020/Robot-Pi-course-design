#!/usr/bin/python3


# -----------------------------------------------------
# Function: Socket Settings (TCP) for Server (Rasp-Pi)
# Coding: utf-8
# -----------------------------------------------------


# ------------- Import necessary packages -------------
import socket
from sys import exit
import GlobalVar as gv
import ThreadSetting as tds
import WheelCtrl as wc
import PCA9685 as pca


# ------- Create functions for wheel controling -------

# Initialize TCP settings on server
def tcpInit(IP, PORT):
    # Define global variables
    global codeMode
    global clientSocket
    global clientIp
    global clientAddr
    gv.setVal("exitFlag", 0)
    print("Starting socket: TCP...\r\n")
    hostAddr = (IP, PORT)
    # Initialize object
    codeMode = "utf-8"                                                          # Encode/decode format
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Create socket object
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)       # Set port reuse
    serverSocket.bind(hostAddr)                                                 # Bind socket to address and port
    serverSocket.listen(1)                                                      # Listen connection request
    print("Listening ...\r\n")
    # Connect with client
    clientSocket, (clientIp, clientPort) = serverSocket.accept()                # Wait for client's connection
    print("Connection accepted from %s, port %s\r\n" %(clientIp, clientPort))
    welcMsg = "Welcome to RPi TCP server!"
    clientSocket.send(welcMsg.encode(codeMode))

# Receive data from client
def recvData():
    while True:
        try:
            # Receive 64 bytes a time
            data = clientSocket.recv(64).decode(codeMode)
            # If data length > 0, then deal with received message 
            if len(data):
                tds.lockAquire()
                print("Client (PC): %s\r\n" %data)
                # Deal with exit message
                if data == 'exit':
                    gv.setVal("exitFlag", 1)
                    clientSocket.close()
                    break
                # Deal with wheel control command
                elif data == 'forward' or data == 'backward' \
                    or data == 'left' or data == 'right' \
                    or data == 'stop':
                    avoidFlag = gv.getVal("avoidFlag")
                    if avoidFlag == 1 and data == "forward":
                        pass
                    else:
                        wc.moveCtrl(data)
                # Deal with camera servo control command
                elif data == "up" or data == "down" \
                    or data =="left" or data == "right":
                        pca.servoCtrl(data)
                tds.lockRelease()
            continue
        except Exception:
            clientSocket.close()
            exit(1)

# Send data to client
def sendData(sendData):
    # Deal with data sending event
    if len(sendData):
        clientSocket.send(sendData.encode(codeMode))    # Send data