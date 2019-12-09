from Tkinter import *
from LowLevelGUI import *
import time

PRESS_TO_ACTIVATE_DURATION_MS = 1500
PRESS_TO_DEACTIVATE_DURATION_MS = 2000
LIGHT_OFF_DURATION_MS = 2000
AUTO_FINISH_EDIT_AFTER_MS = 5000


class DWatchGUI:
    def __init__(self, parent, eventhandler):
        self.GUI = LowLevelGUI(parent, self)

        self.eventhandler = eventhandler

        self.parent = parent

        self.handleEventOn

        self.active_mode = None

        self.is_bottom_right_pressed = False
        self.is_bottom_left_pressed = False

        self.to_edit_time_in_progress = False
        # self.to_edit_alarm_in_progress = False
        self.is_chrono_running = False

        self.end_auto_finish_edit_time_timer = None
        self.finish_edit_time_timer = None

        self.end_auto_finish_alarm_mode_timer = None
        self.finish_alarm_mode_timer = None

        self.light_off_timer = None

        self.is_alarm_on = False
        self.is_alarm_active = False
        self.is_alarm_light_on = False

    def handleEventOn(self):
        self.eventhandler.event('on')

    def wait(self):
        self.eventhandler.event('lightOff2')
        print('wait')

    # -----------------------------------
    # Events to be sent to the Statechart
    # -----------------------------------

    def topLeftPressed(self):
        print('topLeftPressed')
        self.eventhandler.event('stopActiveAlarm')
        self.eventhandler.event('changeMode', self.getActiveMode())
        self.eventhandler.event('selectNext')

    def bottomLeftPressed(self):
        print('bottomLeftPressed')
        self.eventhandler.event('stopActiveAlarm')
        self.eventhandler.event('resetChrono')
        self.eventhandler.event('increase')
        self.setBottomLeftPressed(True)
        self.eventhandler.event('setAlarm')

    def bottomRightPressed(self):
        self.eventhandler.event('stopActiveAlarm')
        self.eventhandler.event('bottomRightPressed')
        self.eventhandler.event('initChrono')
        self.maybeEditTime()
        self.maybeFinishEditTime()

    def topRightPressed(self):
        self.eventhandler.event('stopActiveAlarm')
        self.eventhandler.event('lightOn')
        self.endLightOffTimer()
        print('topRightPressed')

    def topLeftReleased(self):
        print('topLeftReleased')
        self.eventhandler.event('stopActiveAlarm')
        self.eventhandler.event('topLeftReleased')

    def bottomLeftReleased(self):
        print('bottomLeftReleased')
        self.eventhandler.event('stopInc')
        self.eventhandler.event('onoff')
        self.eventhandler.event('bottomLeftReleased')
        self.setBottomLeftPressed(False)

    def bottomRightReleased(self):
        self.setBottomRightPressed(False)
        self.eventhandler.event('released')

    def topRightReleased(self):
        self.startLightOffTimer()
        print('topRightReleased')

    def maybeEditTime(self):
        self.setBottomRightPressed(True)
        self.parent.after(PRESS_TO_ACTIVATE_DURATION_MS, self.tryActivateEditTime)

    def maybeFinishEditTime(self):
        self.setBottomRightPressed(True)
        self.finish_edit_time_timer = self.parent.after(PRESS_TO_DEACTIVATE_DURATION_MS, self.tryFinishEditTime)

    def tryActivateEditTime(self):
        if self.getBottomRightPressed():
            self.eventhandler.event('editTime')

    def tryFinishEditTime(self):
        if self.getBottomRightPressed():
            self.finishEditTime()

    def finishEditTime(self):
        self.eventhandler.event('finishEdit')

    def maybeEditAlarm(self):
        self.setBottomLeftPressed(True)
        self.parent.after(PRESS_TO_ACTIVATE_DURATION_MS, self.tryActivateEditAlarm)

    def tryActivateEditAlarm(self):
        if self.getBottomLeftPressed():
            self.eventhandler.event('editAlarm')

    def maybeFinishAlarmMode(self):
        self.setBottomRightPressed(True)
        self.finish_alarm_mode_timer = self.parent.after(PRESS_TO_DEACTIVATE_DURATION_MS, self.tryFinishAlarmMode)

    def tryFinishAlarmMode(self):
        if self.getBottomRightPressed():
            self.finishAlarmMode()

    def finishAlarmMode(self):
        self.eventhandler.event('finishAlarmMode')

    def setToEditTimeInProgress(self, to_edit_time_in_progress):
        self.to_edit_time_in_progress = to_edit_time_in_progress

    def getToEditTimeInProgress(self):
        return self.to_edit_time_in_progress

    def alarmStart(self):
        self.eventhandler.event('alarming')
        # TODO: pause timers
        print('alarmStart')

    def lightOff(self):
        self.eventhandler.event('lightOff')

    def debug(self):
        self.eventhandler.event('GUI Debug')

    # -----------------------------------
    # Getters/Setters
    # -----------------------------------

    def setBottomRightPressed(self, is_pressed):
        self.is_bottom_right_pressed = is_pressed

    def getBottomRightPressed(self):
        return self.is_bottom_right_pressed

    def setBottomLeftPressed(self, is_pressed):
        self.is_bottom_left_pressed = is_pressed

    def getBottomLeftPressed(self):
        return self.is_bottom_left_pressed

    def getIncreasePressed(self):
        return self.getBottomLeftPressed()

    def getIsAlarmOn(self):
        return self.is_alarm_on

    def getIsAlarmActive(self):
        return self.is_alarm_active

    def setIsAlarmActive(self, is_active):
        self.is_alarm_active = is_active

    # Query
    def getTime(self):
        return self.GUI.getTime()

    def getAlarm(self):
        return self.GUI.getAlarm()
    # -----------------------------------
    # Interaction with the GUI elements
    # -----------------------------------
    # Modify the state:

    def setActiveMode(self, mode):
        self.active_mode = mode

    def getActiveMode(self):
        return self.active_mode

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

    def resetChrono(self):
        self.GUI.resetChrono()

    def increaseChronoByOne(self):
        self.GUI.increaseChronoByOne()

    def setChrono(self, chrono_running):
        self.is_chrono_running = chrono_running

    def getChrono(self):
        return self.is_chrono_running

    # Select current display:
    def startSelection(self):
        self.GUI.startSelection()

    def selectNext(self):
        self.GUI.selectNext()

    # Modify the state corresponing to the selection
    def increaseSelection(self):
        self.GUI.increaseSelection()

    def stopSelection(self):
        self.GUI.stopSelection()

    # Light / Alarm:
    def setIndiglo(self):
        self.GUI.setIndiglo()

    def unsetIndiglo(self):
        self.GUI.unsetIndiglo()

    # Toggle
    def setAlarm(self):
        self.is_alarm_on = not self.is_alarm_on
        self.GUI.setAlarm()

    def blink(self):
        if self.is_alarm_light_on:
            self.unsetIndiglo()
        else:
            self.setIndiglo()
        self.is_alarm_light_on = not self.is_alarm_light_on

    # Check if time = alarm set time
    def checkTime(self):
        if (
                self.GUI.getTime()[0] == self.GUI.getAlarm()[0] and
                self.GUI.getTime()[1] == self.GUI.getAlarm()[1] and
                self.GUI.getTime()[2] == self.GUI.getAlarm()[2]
        ):
            return True
        else:
            return False

    # ------
    # Timers
    # ------
    def startLightOffTimer(self):
        self.light_off_timer = self.parent.after(LIGHT_OFF_DURATION_MS, self.lightOff)

    def endLightOffTimer(self):
        if self.light_off_timer is not None:
            self.parent.after_cancel(self.light_off_timer)

    def startAutoFinishEditTimeTimer(self):
        self.end_auto_finish_edit_time_timer = self.parent.after(AUTO_FINISH_EDIT_AFTER_MS, self.finishEditTime)

    def endAutoFinishEditTimeTimer(self):
        self.parent.after_cancel(self.end_auto_finish_edit_time_timer)

    def endFinishEditTimeTimer(self):
        self.parent.after_cancel(self.finish_edit_time_timer)

    def startAutoFinishAlarmModeTimer(self):
        self.end_auto_finish_alarm_mode_timer = self.parent.after(AUTO_FINISH_EDIT_AFTER_MS, self.finishAlarmMode)

    def endAutoFinishAlarmModeTimer(self):
        if self.end_auto_finish_alarm_mode_timer is not None:
            self.parent.after_cancel(self.end_auto_finish_alarm_mode_timer)
