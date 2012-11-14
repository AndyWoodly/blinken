__author__ = 'andreashz'

import RPi.GPIO as GPIO

import Display

PINS = [2,3,4,17,27,22,23,10,9,14,15,18]
DATAPINS = [3,4,17,27,22,23,10,9]
DATASTROBE = 2
STROBE = 14
OUTEN = 15
AUTOFEED = 18

class RaspiDisplay(Display):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # set output pins
        for pin in PINS:
            GPIO.setup(pin, GPIO.OUT)
        # clear display
        GPIO.output(STROBE, True)
        GPIO.output(OUTEN, True)
        self.clear()

    def clock(self):
        GPIO.output(AUTOFEED, False)
        GPIO.output(AUTOFEED, True)

    def move(self):
        for i in range(16):
            self.clock()

    def setData(self, data):
        for i in range(len(DATAPINS)):
            GPIO.output(DATAPINS[i], (data >> i) & 1)

    def clear(self):
        self.setData(0)
        GPIO.output(DATASTROBE, False)
        self.move()

    def all(self):
        self.setData(255)
        GPIO.output(DATASTROBE, True)
        self.move()

    def delay(self, t):
        if t < MIN_DELAY:
            t = MIN_DELAY
        time.sleep(t)

    def show(self, frame):
        if len(frame) != 8 or len(frame[0]) != 18:
            raise Error, 'Wrong frame dimensions'
        GPIO.output(OUTEN, False)
        self.clear()
        # set secondary ICs data
        for i in range(7,-1,-1):
            data = 0
            for j in range(7,-1,-1):
                data = data << 1
                data = data | frame[i][1+2*j]
            self.setData(data)
            GPIO.output(DATASTROBE, frame[i][17])
            self.clock()
            #time.sleep(0.5)

        # set primary ICs data
        for i in range(7,-1,-1):
            data = 0
            for j in range(7,-1,-1):
                data = data << 1
                data = data | frame[i][2*j]
            self.setData(data)
            GPIO.output(DATASTROBE, frame[i][16])
            self.clock()
            #time.sleep(0.5)

        GPIO.output(OUTEN, True)
