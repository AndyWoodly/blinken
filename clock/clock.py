#!/usr/local/bin/python

import parallel
import time
from time import localtime, strftime
import os
import sys
import random

# minimum delay (seconds) between frames
MIN_DELAY = 0.015

p = parallel.Parallel()
p.setSelect(1)

def clock():
  p.setAutoFeed(0)
  p.setAutoFeed(1)

def move():
  for i in range(16):
    clock()

def clear():
  p.setData(0)
  p.setDataStrobe(0)
  move()

def all():
  p.setData(255)
  p.setDataStrobe(1)
  move()

def delay(t):
  if t < MIN_DELAY:
    t = MIN_DELAY
  time.sleep(t)

def show(frame):
  if len(frame) != 8 or len(frame[0]) != 18:
    raise Error, 'Wrong frame dimensions'
  p.setSelect(0)
  clear()
  # set secondary ICs data
  for i in range(7,-1,-1):
    data = 0
    for j in range(7,-1,-1):
      data = data << 1
      data = data | frame[i][1+2*j]
    p.setData(data)
    p.setDataStrobe(frame[i][17])
    clock()
    #time.sleep(0.5)
  
  # set primary ICs data
  for i in range(7,-1,-1):
    data = 0
    for j in range(7,-1,-1):
      data = data << 1
      data = data | frame[i][2*j]
    p.setData(data)
    p.setDataStrobe(frame[i][16])
    clock()
    #time.sleep(0.5)
      
  p.setSelect(1)

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

clear()
#exit(1)

chars = parseChars("chars.txt")
colon = chars[":"]

prev_min = 0
next_pos = 1 + (int)(random.random() * 10)
counter = 0
off_x = 0
off_y = 0

while(1):
  counter = counter + 1
  if counter == next_pos:
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
    show(f)

clear()
