#!/usr/bin/python

# ----------------------------------------------------
# Function: Raspi PCA9685 16-Channel PWM Servo Driver
# Coding: utf-8
# ----------------------------------------------------

from time import sleep
import GlobalVar as gv
import math
import smbus

# Registers/etc.
SUBADR1      = 0x02
SUBADR2      = 0x03
SUBADR3      = 0x04
MODE1        = 0x00
PRESCALE     = 0xFE
LED0_ON_L    = 0x06
LED0_ON_H    = 0x07
LED0_OFF_L   = 0x08
LED0_OFF_H   = 0x09
ALLLED_ON_L  = 0xFA
ALLLED_ON_H  = 0xFB
ALLLED_OFF_L = 0xFC
ALLLED_OFF_H = 0xFD

# Initialization
def pcaInit():
    bus = smbus.SMBus(1)
    gv.setVal("gcaBus", bus)
    pcaWrite(MODE1, 0x00)
    setPWMFreq(50)
    global servoAng
    servoAng = 500
    setServoPulse(0,servoAng)

# Write data to register
def pcaWrite(address, reg, value):
    "Writes an 8-bit value to the specified register/address"
    bus = gv.getVal("pcaBus")
    bus.write_byte_data(address, reg, value)

# Read data from I2C device
def pcaRead(address, reg):
    "Read a unsignedbyte from the I2C device"
    bus = gv.getVal("pcaBus")
    result = bus.read_byte_data(address, reg)

def setPWMFreq(freq):
    "Sets the PWM frequency"
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescale = math.floor(prescaleval + 0.5)
    
    oldmode = pcaRead(MODE1)
    newmode = (oldmode & 0x7F) | 0x10        # sleep
    pcaWrite(MODE1, newmode)                # go to sleep
    pcaWrite(PRESCALE, int(math.floor(prescale)))
    pcaWrite(MODE1, oldmode)
    sleep(0.005)
    pcaWrite(MODE1, oldmode | 0x80)
    
def setPWM(channel, on, off):
    "Sets a single PWM channel"
    pcaWrite(LED0_ON_L+4*channel, on & 0xFF)
    pcaWrite(LED0_ON_H+4*channel, on >> 8)
    pcaWrite(LED0_OFF_L+4*channel, off & 0xFF)
    pcaWrite(LED0_OFF_H+4*channel, off >> 8)

def setServoPulse(channel, pulse):
    "Sets the Servo Pulse,The PWM frequency must be 50HZ"
    pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us
    setPWM(channel, 0, pulse)
    
def servoCtrl(cmd):
    if cmd == "left":
        servoAng = servoAng - 10
        setServoPulse(0, servoAng)
    elif cmd == "right":
        servoAng = servoAng + 10
        setServoPulse(0, servoAng)