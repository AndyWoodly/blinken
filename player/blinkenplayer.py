#!/usr/local/bin/python

import parallel
import time
import os
import sys
import random

# minimum delay (seconds) between frames
MIN_DELAY = 0.015

basedir = sys.argv[1]

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

def show(t, frame):
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
  delay(t)

def emptyFrame():
  frame = []
  for i in range(8):
    frame.append([])
  for i in range(8):
    for j in range(18):
      frame[i].append(0) 
  return frame

def parseMovie(f):
  print "Parsing "+f+" ..."
  frames = []
  frame = emptyFrame()
  delay = 0
  inframe = 0
  linenr = 0
  abslinenr = 0
  fh = open(basedir+"/"+f)
  for l in fh:
    line = l.strip()
    if line.startswith("#"):
      pass
    try:
      if line == "":
        if inframe:
          inframe = 0
          frames.append((delay, frame))
      if line.startswith("@"):
        frame = emptyFrame() 
        delay = float(line[1:]) / 1000.0
        inframe = 1
        linenr = 0
      if line.startswith("0") or line.startswith("1"):
        if inframe:
          for j in range(len(line)):
            frame[linenr][j] = int(line[j]) 
          linenr = linenr + 1
    except:
      # drop frame
      print "Error parsing line "+str(abslinenr)
      frame = emptyFrame()
      inframe = 0
    abslinenr = abslinenr + 1 
     
  fh.close()
  return frames
      
movies = []

# main loop
while(1):
  movies = []
  for file in os.listdir(basedir):
    (root, ext) = os.path.splitext(file)
    if ext == ".blm":
      movies.append(file)

  while movies:
    movie = random.choice(movies)
    frames = parseMovie(movie)
    for (d, f) in frames:
      show(d, f)
    movies.remove(movie)

clear()
