
class Msg:          
  def displayMessage(self, text):
    print text
  def displayStatic(self, text):
    print text

m = Msg()
w = Weather.Weather(m)
w.showTemperature()
w.showToday()
w.showForecast()

