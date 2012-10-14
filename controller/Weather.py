#!/usr/local/bin/python

import time
from xml.dom import minidom
import urllib
import sys
import re

class Weather():

  def __init__(self, messenger):
    self.messenger = messenger 

  def getAttr(self, text, attribute):
    return re.sub(r'.*'+attribute+'="(.+?)".*$', r'\1', text).rstrip() 

  def getData(self):
    try:
      usock = urllib.urlopen('http://weather.yahooapis.com/forecastrss?p=GMXX5355&u=c')
      data = usock.readlines()
      usock.close()
      return data
    except Exception, (error):
      print "Failed to get weather data: %s" % (error)
    return None

  def showForecast(self):
    try:
      l = self.getData()
      msg = "... the weather forecast ..."
      msg = msg + "    " + l[34].replace("<br />", "").rstrip() + "    "
      msg = msg + "  " + l[35].replace("<br />", "").rstrip() + "   "
      try:
        msg = msg.encode("latin-1")
      except:
        pass
      self.messenger.displayMessage(msg)
    except Exception, (error):
      try:
        print "Ups, can't display weather: %s, %s" % (msg.encode('utf-8'), error)
      except:
        pass

  def showToday(self):
    try:
      l = self.getData()
      msg = "... the weather today ..."
      msg = msg + "   " + self.getAttr(l[28], "text") + ", "
      msg = msg + self.getAttr(l[28], "temp") + " C, "
      msg = msg + self.getAttr(l[12], "speed") + " km/h, "
      msg = msg + self.getAttr(l[13], "humidity") + " %, "
      msg = msg + self.getAttr(l[13], "pressure") + " mbar "
      msg = msg + "(trend: " + self.getAttr(l[13], "rising") + "), "
      msg = msg + "day: " +  self.getAttr(l[14], "sunrise") + " -> "
      msg = msg + self.getAttr(l[14], "sunset") + " "
      try:
        msg = msg.encode("latin-1")
      except:
        pass
      self.messenger.displayMessage(msg)
    except Exception, (error):
      try:
        print "Ups, can't display weather: %s, %s" % (msg.encode('utf-8'), error)
      except:
        pass

  def showTemperature(self):
    try:
      l = self.getData()
      msg = self.getAttr(l[28], "temp") + "C "
      try:
        msg = msg.encode("latin-1")
      except:
        pass
      self.messenger.displayStatic(msg)
    except Exception, (error):
      try:
        print "Ups, can't display weather: %s, %s" % (msg.encode('utf-8'), error)
      except:
        pass



