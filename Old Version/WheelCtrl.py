#!/usr/bin/python3

# ---------------------------------------
# Wheel control functions definition
# ---------------------------------------

# -------- Import necessary libraries --------
import RPi.GPIO as GPIO
from time import sleep

# -------- Define class for wheel controling --------
class WheelCtrl(object):
    # Initialization
    def __init__(self, ain1=12, ain2=13, ena=6, bin1=20, bin2=21, enb=26):
        # Set pins for controling signals
        self.AIN1 = ain1		# Controling signal 1 of left wheel
        self.AIN2 = ain2		# Controling signal 2 of left wheel
        self.BIN1 = bin1		# Controling signal 1 of right wheel
        self.BIN2 = bin2		# Controling signal 2 of right wheel
        self.ENA = ena			# Enable signal of left wheel
        self.ENB = enb			# Enable signal of right wheel
        self.PA = 20			# PWM duty of left wheel
        self.PB = 20			# PWM duty of right wheel
        # Initialize controling ports
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA, 500)
        self.PWMB = GPIO.PWM(self.ENB, 500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    # ** Function for direction controling **
    #           AIN1 AIN2 BIN1 BIN2
    # Forward    0    1    0    1
    # Back       1    0    1    0
    # Left       1    0    0    1
    # Right      0    1    1    0
    # Stop       0    0    0    0

    def forward(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.HIGH)

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def backward(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.LOW)

    def left(self):
        self.PWMA.ChangeDutyCycle(30)
        self.PWMB.ChangeDutyCycle(30)
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.HIGH)

    def right(self):
        self.PWMA.ChangeDutyCycle(30)
        self.PWMB.ChangeDutyCycle(30)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.LOW)

	# Function for speed controling
	# Left wheel
    def setPWMA(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)
	# Right wheel
    def setPWMB(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)

    # Motor function: combine all movement together
    # 0 <= left <= 100: left wheel forward
    # -100 <= left < 0: left wheel backward
    # 0 <= right <= 100: right wheel forward
    # -100 <= right < 0: right wheel backward
    def setMotor(self, left, right):
        if((left >= 0) and (left <= 100)):
            GPIO.output(self.AIN1, GPIO.LOW)
            GPIO.output(self.AIN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(left)
        elif((left < 0) and (left >= -100)):
            GPIO.output(self.AIN1, GPIO.HIGH)
            GPIO.output(self.AIN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(0 - left)
        if((right >= 0) and (right <= 100)):
            GPIO.output(self.BIN1, GPIO.LOW)
            GPIO.output(self.BIN2, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(right)
        elif((right < 0) and (right >= -100)):
            GPIO.output(self.BIN1, GPIO.HIGH)
            GPIO.output(self.BIN2, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(0 - right)


if __name__ == '__main__':

    Wc = WheelCtrl()
    Wc.forward()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
