import sys
import json

from twisted.internet import reactor
from twisted.python import log

from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS


class WebDisplay(WebSocketServerProtocol):

    def __init__(self):
        log.startLogging(sys.stdout)

        self.factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
        self.factory.protocol = WebDisplay
        listenWS(self.factory)

        reactor.run()

    def onMessage(self, msg, binary):
      print "got message:", msg

    def show(self, frame):
        if len(frame) != 8 or len(frame[0]) != 18:
            raise Error, 'Wrong frame dimensions'
        self.sendMessage(json.dumps(frame))
