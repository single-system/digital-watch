from Tkinter import *
from LowLevelGUI import *
import time

is_bottom_right_pressed = True
to_edit_time_in_progress = True
PRESS_TO_ACTIVATE_DURATION_MS = 1500
PRESS_TO_DEACTIVATE_DURATION_MS = 2000
AUTO_FINISH_EDIT_AFTER_MS = 5000
end_auto_finish_edit_time_timer = None


class DWatchGUI:
  def __init__(self, parent, eventhandler):
    self.GUI = LowLevelGUI(parent, self)

    self.eventhandler = eventhandler

    self.parent = parent

    self.handleEventOn

  def handleEventOn(self):
    self.eventhandler.event("on")

  def wait(self):
    self.eventhandler.event("lightOff2")
    print "wait"

  # -----------------------------------
  # Events to be sent to the Statechart
  # -----------------------------------

  def debug(self):
    self.eventhandler.event('GUI Debug')

  def topRightPressed(self):
    self.eventhandler.event("lightOn")
    print "topRightPressed"

  def topRightReleased(self):
    self.eventhandler.event("lightOff")
    print "topRightReleased"

  def topLeftPressed(self):
    self.eventhandler.event("changeMode")
    self.eventhandler.event('selectNext')

  def topLeftReleased(self):
    print 'topLeftReleased'
    self.eventhandler.event('topLeftReleased')

  def bottomRightPressed(self):
    self.eventhandler.event('bottomRightPressed')
    self.eventhandler.event('initChrono')
    self.maybeEditTime()
    self.maybeFinishEditTime()


  def startAutoFinishEditTimeTimer(self):
    self.end_auto_finish_edit_time_timer = self.parent.after(AUTO_FINISH_EDIT_AFTER_MS, self.finishEditTime)


  def endAutoFinishEditTimeTimer(self):
    self.parent.after_cancel(self.end_auto_finish_edit_time_timer)


  def maybeEditTime(self):
    self.is_bottom_right_pressed = True
    self.parent.after(PRESS_TO_ACTIVATE_DURATION_MS, self.tryActivateEditTime)


  def maybeFinishEditTime(self):
    self.is_bottom_right_pressed = True
    self.parent.after(PRESS_TO_DEACTIVATE_DURATION_MS, self.tryFinishEditTime)

  def tryActivateEditTime(self):
    if self.is_bottom_right_pressed:
      self.eventhandler.event('editTime')


  def tryFinishEditTime(self):
    if self.is_bottom_right_pressed:
      self.finishEditTime()


  def finishEditTime(self):
    self.eventhandler.event('finishEdit')


  def setToEditTimeInProgress(self, to_edit_time_in_progress):
    self.to_edit_time_in_progress = to_edit_time_in_progress


  def getToEditTimeInProgress(self):
    return self.to_edit_time_in_progress


  def bottomRightReleased(self):
    self.is_bottom_right_pressed = False
    self.eventhandler.event('released')


  def bottomLeftPressed(self):
    self.eventhandler.event("resetChrono")
    self.eventhandler.event("increase")
    self.eventhandler.event("setAlarm")

  def bottomLeftReleased(self):
    self.eventhandler.event('stopInc')
    self.eventhandler.event('onoff')
    self.eventhandler.event('bottomLeftReleased')
    print 'bottomLeftReleased'

  def alarmStart(self):
    self.eventhandler.event("alarming")
    print "alarmStart"

  # -----------------------------------
  # Interaction with the GUI elements
  # -----------------------------------
  #Modify the state:

  def refreshTimeDisplay(self):
    self.GUI.drawTime()

  def refreshChronoDisplay(self):
    self.GUI.drawChrono()

  def refreshDateDisplay(self):
    self.GUI.drawDate()

  def refreshAlarmDisplay(self):
    self.GUI.drawAlarm()

  def increaseTimeByOne(self):
    self.GUI.increaseTimeByOne()
    self.refreshTimeDisplay()

  def resetChrono(self):
    self.GUI.resetChrono()

  def increaseChronoByOne(self):
    self.GUI.increaseChronoByOne()

  # Select current display:

  def startSelection(self):
    self.GUI.startSelection()

  def selectNext(self):
    self.GUI.selectNext()

  #Modify the state corresponing to the selection
  def increaseSelection(self):
    self.GUI.increaseSelection()

  def stopSelection(self):
    self.GUI.stopSelection()


  #Light / Alarm:

  def setIndiglo(self):
    self.GUI.setIndiglo()

  def unsetIndiglo(self):
    self.GUI.unsetIndiglo()

  def setAlarm(self):
    self.GUI.setAlarm()

  # Query
  def getTime(self):
    return self.GUI.getTime()

  def getAlarm(self):
    return self.GUI.getAlarm()

  #Check if time = alarm set time
  def checkTime(self):
    if self.GUI.getTime()[0] == self.GUI.getAlarm()[0] and self.GUI.getTime()[1] == self.GUI.getAlarm()[1] and self.GUI.getTime()[2] == self.GUI.getAlarm()[2]:
      return True
    else:
      return False

