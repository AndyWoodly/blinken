#!/usr/bin/python

import RPi.GPIO as GPIO

import time
from time import localtime, strftime
import os
import sys
import random
import Messenger
import Weather

# minimum delay (seconds) between frames
MIN_DELAY = 0.015

PINS =   [2,3,4,17,27,22,23,10,9,14,15,18]
DATAPINS = [3,4,17,27,22,23,10,9]
DATASTROBE = 2
STROBE = 14
OUTEN = 15
AUTOFEED = 18

class Display():

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

  def emptyMatrix(self,y,x):
    return emptyMatrix(y,x)

def emptyMatrix(y,x):
  frame = []
  for i in range(y):
    frame.append([])
  for i in range(y):
    for j in range(x):
      frame[i].append(0) 
  return frame


def parseChars(f):
  print "Parsing character file "+f+" ..."
  chars = {}
  fh = open(f)
  c = ""
  frame = emptyMatrix(5,3)
  linenr = 0
  for l in fh:
    line = l.strip()
    if line.startswith("#"):
      c = line[1:].strip()
    elif line == "":
      #print "parsed character: "+c
      chars[c] = frame
      frame = emptyMatrix(5,3)
      linenr = 0
    elif line.startswith("0") or line.startswith("1"):
      for j in range(len(line)):
        frame[linenr][j] = int(line[j]) 
      linenr = linenr + 1
       
  fh.close()
  return chars

def skewTime(h, m, s):
  return (h,m,s)

# main loop

chars = parseChars("clock_chars.txt")
colon = chars[":"]

display = Display()

# load messenger module
messenger = Messenger.Messenger(display)
weather = Weather.Weather(messenger)
#weather.showToday()
#messenger.showNews()

prev_min = 0
next_pos = 1 + (int)(random.random() * 10)
counter = 0
off_x = 0
off_y = 0


while(1):
  counter = counter + 1
  if counter == next_pos:
    if counter % 3 == 0:
      weather.showTemperature()
      time.sleep(5)
    counter = 0
    next_pos = 1 + (int)(random.random() * 100)
    off_y = (int)(random.random() * 4)
    off_x = (int)(random.random() * 2)
  time.sleep(1)
  t = strftime("%H:%M:%S", localtime())
  (h,m,s) = t.split(":")
  (h,m,s) = skewTime(h, m, s)
  if counter == 0 or prev_min != m:
    prev_min = m
    f = emptyMatrix(8,18)
    h1 = chars[h[0]]
    h2 = chars[h[1]]
    m1 = chars[m[0]]
    m2 = chars[m[1]]
    for i in range(5):
      for j in range(3):
        # update frame
        f[i+off_y][j+off_x] = h1[i][j]
        f[i+off_y][j+off_x+4] = h2[i][j]
        f[i+off_y][j+off_x+7] = colon[i][j]
        f[i+off_y][j+off_x+10] = m1[i][j]
        f[i+off_y][j+off_x+14] = m2[i][j]
    display.show(f)
  if m == "00" and s == "00":
    messenger.displayMessage("... the news ...")
    try:
      messenger.showNews()
    except Exception, (error):
      print "Can't show news: %s" % (error)
      pass
  if m == "30" and s == "00":
    try:
      weather.showToday()
      weather.showForecast()
    except Exception, (error):
      print "Can't show forecast: %s" % (error)
      pass

display.clear()
