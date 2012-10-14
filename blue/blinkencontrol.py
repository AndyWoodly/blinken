#!/usr/bin/python2.4

import parallel
import time
import os
import sys
import random
from bluetooth import *

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
  if delay == -1:
    return 
  if t < MIN_DELAY:
    t = MIN_DELAY
  time.sleep(t)

def show(t, frame):
  p.setSelect(0)
  if t != -1:
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

# bluetooth connection loop
while True:                     
  clear()
  x = 0
  y = 0
  prev = 0
  frame = emptyFrame()
  #frame[x][y] = 1
  #show(-1, frame)
  
  server_sock=BluetoothSocket( RFCOMM )
  server_sock.bind(("",PORT_ANY))
  server_sock.listen(1)
  
  port = server_sock.getsockname()[1]
  
  uuid = "1234"
  
  advertise_service( server_sock, "homecontrol",
                     service_id = uuid,
                     service_classes = [ uuid, SERIAL_PORT_CLASS ],
                     profiles = [ SERIAL_PORT_PROFILE ] )
  
  print "Waiting for connection on RFCOMM channel %d" % port
  
  client_sock, client_info = server_sock.accept()
  print "Accepted connection from ", client_info
  
  c_up = 255
  c_down = 254
  c_left = 252
  c_right = 253
  c_toggle = 49
  
  try:
      while True:
          data = client_sock.recv(8)
          d = ord(data)
          #print d
          if d == c_toggle:
            prev = abs(prev-1)
            continue
          frame[x][y] = prev
          if d == c_up: x = x + 1
          if d == c_down: x = x - 1
          if d == c_left: y = y - 1
          if d == c_right: y = y + 1
          if x == 8: x = 0
          if x == -1: x = 7
          if y == 18: y = 0
          if y == -1: y = 17
          prev = frame[x][y]
          frame[x][y] = 1
          show(-1, frame)
  except IOError:
      pass
  
  print "disconnected"
  clear()
  
  client_sock.close()
  server_sock.close()
