#!/usr/local/bin/python

from time import localtime, strftime
import json
import urllib

class Tide():

  def __init__(self, messenger):
    self.messenger = messenger 
    self.cache = {}

  def getData(self):
    try:
      t = strftime("%H:%M:%S", localtime())
      (h,m,s) = t.split(":")
      cached = self.cache.get(h)
      if cached is not None:
        return cached
      usock = urllib.urlopen('http://api.spitcast.com/api/county/tide/santa-cruz/')
      data = json.loads(usock.read())
      usock.close()
      self.cache[h] = data
      return data
    except Exception, error:
      print "Failed to get tide data: %s" % (str(error))
    return []

  def showTide(self):
    try:
      d = self.getData()
      tide = map(lambda x: int(round(x["tide"])), d) 
      frame = self.messenger.emptyFrame()
      for y in range(18): 
        t = tide[y]
        for x in range(t):
          x_inv = max(7-x,0)
          frame[x_inv][y] = 1
      self.messenger.showFrame(frame)
    except Exception, error:
      print "Ups, can't messenger tide information: %s" % (str(error))

