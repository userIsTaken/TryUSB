from PyQt5 import QtCore, QtWidgets, QtGui
from UIfiles.GUIThread import Ui_MainGuiWindow
import datetime as dt

def SetupWindow(gui:Ui_MainGuiWindow):
        # icons:

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        gui.actionI_saugoti_DAT.setIcon(icon2)
        gui.actionI_saugoti_TXT.setIcon(icon2)
        gui.actionI_saugoti_QTI_projekt.setIcon(icon2)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Icons/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        gui.findAllUSBTMC_devices_button.setIcon(icon3)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        gui.actionU_daryti.setIcon(icon4)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Icons/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        gui.anotherExitButton.setIcon(icon5)
        #  insert current date:
        cDate = dt.datetime.now()
        gui.dateEdit.setDate(cDate)
        # print(cDate)
        gui.dataViewWidget.plotItem.showGrid(True, True, 1.0)
        gui.experimentDataViewPlot.plotItem.showGrid(True, True, 1.0)
        pass

def SweepButtonsFunctionality(gui:Ui_MainGuiWindow):
        '''

        :param gui: Main Widget of window
        :return:
        '''
        if gui.sweepAmplitudeRadioButton.isChecked():
                #enable controls for amplitude sweep:
                gui.startAmplitudeSweepBox.setEnabled(True)
                gui.stopAmplitudeSweepBox.setEnabled(True)
                gui.fixedOffsetBox.setEnabled(True)
                gui.stepForAmplitudeSweepBox.setEnabled(True)
                gui.timeForAmplOffsSweepBox.setEnabled(True)
                gui.groupBoxForSweepAO.setEnabled(True)
                # disable controls for Offset and time sweeps:
                gui.startOffsetSweepBox.setEnabled(False)
                gui.stopOffsetSweepBox.setEnabled(False)
                gui.stepForOffsetSweep.setEnabled(False)
                gui.fixedAmplitudeBox.setEnabled(False)
                #
                gui.startTimeSweepBox.setEnabled(False)
                gui.stopTimeSweepBox.setEnabled(False)
                gui.stepForTimeSweepBox.setEnabled(False)
                gui.groupBoxForSwepTime.setEnabled(False)
                gui.fixedAmplTimeSweepBox.setEnabled(False)
                gui.fixedOffsTimeSweepBox.setEnabled(False)
                print("Sweep Ampl")
                # fill information from Generator tab:
                amplitude = gui.voltageAmplitudeBox.value()
                offset = gui.voltageOffsetBox.value()
                period = gui.periodBox.value()
                start_amplitude = amplitude
                stop_amplitude = amplitude + 2.0
                start_offset = offset;
                stop_offset = offset + 2.0
                period_start = period
                period_stop = period + 10.0
                pass
        elif gui.sweepOffsetRadioButton.isChecked():
                gui.startOffsetSweepBox.setEnabled(True)
                gui.stopOffsetSweepBox.setEnabled(True)
                gui.stepForOffsetSweep.setEnabled(True)
                gui.fixedAmplitudeBox.setEnabled(True)
                gui.timeForAmplOffsSweepBox.setEnabled(True)
                gui.groupBoxForSweepAO.setEnabled(True)
                print("Sweep OFFS")
                #
                gui.startAmplitudeSweepBox.setEnabled(False)
                gui.stopAmplitudeSweepBox.setEnabled(False)
                gui.fixedOffsetBox.setEnabled(False)
                gui.stepForAmplitudeSweepBox.setEnabled(False)
                #
                gui.startTimeSweepBox.setEnabled(False)
                gui.stopTimeSweepBox.setEnabled(False)
                gui.stepForTimeSweepBox.setEnabled(False)
                gui.groupBoxForSwepTime.setEnabled(False)
                gui.fixedAmplTimeSweepBox.setEnabled(False)
                gui.fixedOffsTimeSweepBox.setEnabled(False)
                # fill information from Generator tab:
                amplitude = gui.voltageAmplitudeBox.value()
                offset = gui.voltageOffsetBox.value()
                period = gui.periodBox.value()
                start_amplitude = amplitude
                stop_amplitude = amplitude + 2.0
                # start_offset = offset;
                # stop_offset = offset + 2.0
                # period_start = period
                # period_stop = period + 10.0
                gui.startAmplitudeSweepBox.setValue(start_amplitude)
                gui.stopAmplitudeSweepBox.setValue(stop_amplitude)
                gui.fixedOffsetBox.setValue(offset)
                gui.timeForAmplOffsSweepBox.setValue(period)
                if gui.periodRadioButton_mS.isChecked():
                        gui.time_unit_mS.setChecked(True)
                elif gui.periodRadioButton_uS.isChecked():
                        gui.time_unit_uS.setChecked(True)
                        pass
                elif gui.periodradioButton_S.isChecked():
                        gui.time_unit_S.setChecked(True)
                        pass
                else:
                        print("Some shit happens")
                pass
        elif gui.sweepTimeRadioButton.isChecked():
                gui.startTimeSweepBox.setEnabled(True)
                gui.stopTimeSweepBox.setEnabled(True)
                gui.stepForTimeSweepBox.setEnabled(True)
                gui.groupBoxForSwepTime.setEnabled(True)
                gui.fixedAmplTimeSweepBox.setEnabled(True)
                gui.fixedOffsTimeSweepBox.setEnabled(True)
                print("Sweep time")
                #
                gui.startAmplitudeSweepBox.setEnabled(False)
                gui.stopAmplitudeSweepBox.setEnabled(False)
                gui.fixedOffsetBox.setEnabled(False)
                gui.stepForAmplitudeSweepBox.setEnabled(False)
                gui.timeForAmplOffsSweepBox.setEnabled(False)
                gui.groupBoxForSweepAO.setEnabled(False)
                #
                gui.startOffsetSweepBox.setEnabled(False)
                gui.stopOffsetSweepBox.setEnabled(False)
                gui.stepForOffsetSweep.setEnabled(False)
                gui.fixedAmplitudeBox.setEnabled(False)
                # fill information from Generator tab:
                amplitude = gui.voltageAmplitudeBox.value()
                offset = gui.voltageOffsetBox.value()
                period = gui.periodBox.value()
                start_amplitude = amplitude
                stop_amplitude = amplitude + 2.0
                start_offset = offset
                stop_offset = offset + 2.0
                period_start = period
                period_stop = period + 10.0
                pass
        else:
                print("Some shit in SweepButtonsFunctionality")
        pass