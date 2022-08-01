# -----------------------------------------------
# Function: Socket Settings (TCP) for Client (PC)
# Coding: utf-8
# -----------------------------------------------


# ------------- Import necessary packages -------------
import socket
from sys import exit
import ThreadSetting as tds
import GlobalVar as gv


# ------- Create functions for wheel controling -------

# Initialize TCP settings on server
def tcpInit(IP, PORT):
    # Define global variables
    global codeMode
    global clientSocket
    gv.setVal("exitFlag", 0)
    print("Starting socket: TCP...\r\n")
    serverAddr = (IP, PORT)
    # Initialize object
    codeMode = "utf-8"                                                          # Encode/decode format
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Create socket object
    print("Connecting to server @ %s: %d ...\r\n" %(IP, PORT))
    # Connect to server
    clientSocket.connect(serverAddr)
    print("Connect successful!")
    # Receive welcome message
    welcMsg = clientSocket.recv(64)
    if len(welcMsg) > 0:
        print("Received: %s" %welcMsg.decode(codeMode))
    else:
        print("ERROR! Welcome message missed!\r\n")
    print("Use keyboard to control the car...\r\n")

# Receive data from server
def recvData():
    while True:
        try:
            # Receive 64 bytes a time
            data = clientSocket.recv(64).decode(codeMode)
            # If data length > 0, then deal with received message 
            if len(data):
                print("Server (Robot Pi): %s\r\n" %data)
                # Deal with obstacle event
                if data == 'obstacle' or data == 'avoided':
                    if data == 'obstacle':
                        forwardLock = 1
                    else:
                        forwardLock = 0
                    gv.setVal("forwardLock", forwardLock)
            continue
        except Exception:
            clientSocket.close()
            exit(1)

# Send data to server
def sendData(sendData):
    # Deal with data sending event
    if len(sendData):
        clientSocket.send(sendData.encode(codeMode))    # Send data