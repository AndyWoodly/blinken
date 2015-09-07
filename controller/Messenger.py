#!/usr/local/bin/python

import time
import feedparser

class Messenger():

  def __init__(self, display):
    self.display = display 
    self.chars = self.parseChars("chars.txt")
    k = self.chars.keys()
    k.sort()
    s = "".join(k)
    print s
    #self.displayMessage(s)

  def appendFrame(self, frame, appendix, y_offset=0, space=0):
    y = len(frame)
    x_f = len(frame[0])
    x_a = len(appendix[0])
    x = x_f + x_a + space
    res = self.display.emptyMatrix(y, x)
    for i in range(y):
      # copy frame
      for j in range(x_f):
        res[i][j] = frame[i][j]
      # append
      if i < len(appendix):
        for j in range(x_a):
          #print "len(res): "+str(len(res)),"i: "+str(i),"y_offset: "+str(y_offset),"j: "+str(j),"x_f: "+str(x_f),"space: "+str(space),"len(appendix): "+str(len(appendix)),"len(appendix[i]): "+str(len(appendix[i]))
          res[i+y_offset][j+x_f+space] = appendix[i][j]
    return res

  def clip(self, frame, dim, offset):
    assert len(frame[0]) >= dim + offset
    y = len(frame)
    res = self.display.emptyMatrix(y, dim)
    for i in range(y):
      for j in range(dim):
        res[i][j] = frame[i][j+offset]
    return res 

  def parseChars(self, file):
    """parse chars into a variable dimension frame"""
    Y = 7
    X = 4
    print "Parsing character file "+file+" ..."
    chars = {}
    fh = open(file)
    c = ""
    #frame = self.display.emptyMatrix(Y,X)
    linenr = 0
    matrix_starts = 0
    for l in fh:
      line = l.strip()
      if line.startswith("#"):
        c = line[2:3]
        #print "parsing <"+c+">"
        matrix_starts = 1
      elif line == "":
        print "parsed character: "+c
        #for u in range(Y-linenr+1):
        #  frame.pop()
        chars[c] = frame
        #printFrame(frame)
        #frame = self.display.emptyMatrix(Y,X)
        linenr = 0
      elif line.startswith("0") or line.startswith("1"):
        if matrix_starts:
          frame = self.display.emptyMatrix(Y,len(line))
          matrix_starts = 0
        for j in range(len(line)):
          #print "linenr: "+str(linenr), "x: "+str(j), "value: "+str(int(line[j])), "|", len(frame), len(frame[linenr])
          frame[linenr][j] = int(line[j]) 
        linenr = linenr + 1
       
    fh.close()
    return chars

  def getChar(self, c):
    if c == " ":
      return self.display.emptyMatrix(7,3)
    if self.chars.has_key(c):
      return self.chars[c]
    else:
      return self.display.emptyMatrix(7,3)

  def printFrame(self, frame):
    """Print out frame for debugging"""
    print
    for i in range(len(frame)):
      for j in range(len(frame[0])):
        if frame[i][j] == 1:
          print "#",
        else:
          print " ",
      print

  def emptyFrame(self):
    return self.display.emptyMatrix(8,18)

  def showFrame(self, frame):
    self.display.show(frame)

  def displayMessage(self, message):
    msg = message + "      "
    screen = self.display.emptyMatrix(8,18)
    off_screen = self.display.emptyMatrix(8,18)
    run = 1

    m_pos = 0
    c_shift = 0
    c_stop = 0

    ch = ""
    while(run):
      if c_shift == c_stop:
        off_screen = self.clip(off_screen, 18, c_stop)
        c_shift = 0
        ch = self.getChar(msg[m_pos])
        m_pos = m_pos + 1
        c_stop = len(ch[0]) + 1
        off_screen = self.appendFrame(off_screen, ch, 1, 1)
        #printFrame(off_screen)
        
      screen = self.clip(off_screen, 18, c_shift)  
      time.sleep(0.03)
      #printFrame(screen)
      self.display.show(screen)
      c_shift = c_shift + 1
      if m_pos == len(msg)-1:
        run = 0

    self.display.clear()

  def displayStatic(self, message):
    screen = self.display.emptyMatrix(8,18)
    count = 0;
    for i in range(len(message)):
      ch = self.getChar(message[i])
      count = count + len(ch[0]) + 1
      screen = self.appendFrame(screen, ch, 1, 1)
    screen = self.clip(screen, 18, count)
    self.display.show(screen)

  def showNews(self):
    try:
      print "Retrieving news ..."
      news = feedparser.parse("http://news.google.de/?output=rss")
      for e in news.entries:
        msg = e.title
        # remove news source
        idx = msg.rfind("-")
        if idx != -1:
          msg = msg[:idx].strip()
        #msg = msg.decode('utf-8')
        #msg = msg.encode('iso-8859-1', 'replace')
        msg = msg.replace("&quot;", "'")
        try:
          msg = msg.encode("latin-1")
        except:
          pass
        print msg
        print
        #self.displayMessage(msg.upper())
        self.displayMessage(msg)
    except Exception, (error):
      try:
        print "Ups, can't display message: %s, %s" % (msg.encode('utf-8'), error)
      except:
        pass
      return

### package methods

def printFrame(frame):
  """Print out frame for debugging"""
  print
  for i in range(len(frame)):
    for j in range(len(frame[0])):
      if frame[i][j] == 1:
        print "#",
      else:
        print " ",
    print

