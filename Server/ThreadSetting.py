#!/usr/bin/python3


# ---------------------------------------
# Function: Threading Settings
# Coding: utf-8
# ---------------------------------------


# ------------- Import necessary packages -------------
from threading import Lock


# ------ Create functions for threading settings ------

# Initialization
def threadInit():
    global threadlock
    threadlock = Lock()

# Aquire threading lock
def lockAquire():
    threadlock.acquire()

# Release threading lock
def lockRelease():
    threadlock.release()