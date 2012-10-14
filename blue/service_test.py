#!/usr/local/bin/python

import parallel
import time
import os
import sys
import random

from bluetooth import *

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
c_left = 253
c_right = 252

try:
    while True:
        data = client_sock.recv(8)
        d = ord(data)
        if d == c_up: print "up"
        if d == c_down: print "down"
        if d == c_left: print "left"
        if d == c_right: print "right"
except IOError:
    pass

print "disconnected"

client_sock.close()
server_sock.close()
