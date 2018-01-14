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
                #

                print("Sweep Ampl")
                pass
        elif gui.sweepOffsetRadioButton.isChecked():
                print("Sweep OFFS")
                #
                pass
        elif gui.sweepTimeRadioButton.isChecked():
                print("Sweep time")
                #
                pass
        else:
                print("Some shit in SweepButtonsFunctionality")
        pass