#!/usr/bin/python3
#-*- coding: utf-8-*-
from PyQt5 import QtCore, QtWidgets, QtGui
from UIfiles.GUIThread import Ui_MainGuiWindow

import sys, os
from Oscilographs.USBTMC_Devices import *
from Oscilographs.TektronixScope import *
from GetInfoAboutDevices import *
from ConfigParser import *
import vxi11
import random
import pyqtgraph as pG
from pyqtgraph import exporters

from Units.MeasurementData import *


from Generators.SiglentGenerator import *
from Generators.TektronixGenerator import *
from MainExperimentLoopThread import *
from DummyFiles.DummyFunctions import *
from Units.UnitCheck import *
from UIfiles.UISetupFunctions import *
from Units.Functions import *
# Very global dictionary for all devices?

# prettier graphs:
pG.setConfigOptions(antialias=True)
# very global variables:
ON = "ON"
OFF = "OFF"
from ThreadedRigolreading import *
import traceback as tb




class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super(MainWindow, self).__init__()
                self.ui = Ui_MainGuiWindow()
                self.ui.setupUi(self)
                #Normally this is all to be done in order to show a window
                self.ThreadPool = QThreadPool() # because of threading?
                self._threads = []
                self._thread = None
                self._worker = None
                self._path = None
                # plots:
                #self._plots = []
                #declare global self.dictionary:
                self.DevicesUSBTMC={} # for USBTMC
                self.DevicesTCP={} # for TCP/IP devices
                # Globals for our devices
                self.Generator = None
                self.Osciloscope = None
                self.PeriodUnit = None
                self.PeriodPower = None
                self.TriggerIntervalUnit = None
                self.TriggerIntervalPower = None
                # set up a table:
                self.setupTable()
                # close functions:
                self.ui.actionU_daryti.triggered.connect(self.closeFn)
                self.ui.closeButton.clicked.connect(self.closeFn)
                self.ui.anotherExitButton.clicked.connect(self.closeFn)
                self.ui.unused_button.clicked.connect(self.unusedFunction)
                self.ui.findAllUSBTMC_devices_button.clicked.connect(self.scan_for_all_USBTMC_devices)
                self.ui.clearErrorTextButton.clicked.connect(self.clearTextInIfoFiel)
                self.ui.addDeviceEntryTableButton.clicked.connect(self.addRowIntoTable)
                self.ui.getIDNfroSelectedIPButton.clicked.connect(self.getIDN_from_selected_table_device)
                self.ui.removeSelectedRowButton.clicked.connect(self.removeSelectedRow)
                self.ui.connectToGeneratorButton.clicked.connect(self.connectGenerator)
                self.ui.runInitiallConfiguration_button.clicked.connect(self.runInitGenerator)
                self.ui.InputOutputCH1Button.clicked.connect(self.changeOutputCH1)
                self.ui.InputOutputCH2Button.clicked.connect(self.changeOutputCH2)
                # Other signals:
                self.ui.connectToOscilograph_button.clicked.connect(self.connectOscilograph)
                self.ui.getVoltsFromCH1_button.clicked.connect(self.getVoltsFromCH1_button_clicked)
                self.ui.getVoltasFromCH2_button.clicked.connect(self.getVoltsFromCH2_button_clicked)
                self.ui.getDatafromBothChannels_button.clicked.connect(self.getDatafromBothChannels_button_clicked)
                self.dataCurveOne = self.ui.dataViewWidget.plot()
                self.dataCurveTwo = self.ui.dataViewWidget.plot()
                #eksperimento kreives:
                #self.ui.startExperimentButton.clicked.connect(self.ekspMatavimas_clicked)
                # self.ekspCurveOne = self.ui.experimentDataViewPlot.plot()
                # self.ekspCurveTwo = self.ui.experimentDataViewPlot.plot()
                self.ekspCurveOne = self.ui.experimentDataPlots.ui.channelOneView.plot()
                self.ekspCurveTwo =  self.ui.experimentDataPlots.ui.channelTwoView.plot()
                #---------------------
                self.SetupWindow()
                self.ui.useRegularUpdateBox.stateChanged.connect(self.StateChanged)
                # everything related to control of generator:
                self.ui.setSignalAmplitudeButton.clicked.connect(self.setGeneratorsAmplitude)
                self.ui.sendCustomCmd_gen_button.clicked.connect(self.sendCustomGenCmd)
                self.ui.setOffsetButton.clicked.connect(self.setOffset_generator)
                self.ui.setPeriodButton.clicked.connect(self.setPeriod_generator)
                self.ui.setTriggerIntervalButton.clicked.connect(self.SetTriggerInterval_gen)
                self.ui.renewGeneratorInfoButton.clicked.connect(self.RenewGeneratorFields)
                self.ui.responseChannelOscBox.currentIndexChanged.connect(self.updateChannelsOsc)
                self.ui.signalChannelOscBox.currentIndexChanged.connect(self.updateChannelsOsc)
                # Main loop:
                self.ui.startExperimentButton.clicked.connect(self.StartExperimentLoop)
                # Configuration saving and loading:
                self.ui.saveEntriesButton.clicked.connect(self.saveEntriesToConfig)
                self.ui.loadEntriesButton.clicked.connect(self.loadEntriesFromConfig)
                self.ui.sweepAmplitudeRadioButton.clicked.connect(self.SetSweepFunctions)
                self.ui.sweepOffsetRadioButton.clicked.connect(self.SetSweepFunctions)
                self.ui.sweepTimeRadioButton.clicked.connect(self.SetSweepFunctions)
                # Oscilograph cmds:
                self.ui.sendCustomCMDoscil.clicked.connect(self.sendCMDintoOcilograph)
                self.ui.fullscreenButton.clicked.connect(self.SetFullScreen)
                #
                self.ui.connectoAllDevicesButton.clicked.connect(self.ConnectToAllDevices)
                #Save functionality
                #path button
                self.ui.path_button.clicked.connect(self.set_path_function)
                self.ui.saveToTXTbutton.clicked.connect(self.saveToTXT_oscillograph_view_function)
                self.ui.saveRawData_button.clicked.connect(self.saveData)
                self.ui.saveRawButton.clicked.connect(self.saveRawExpData)
                # easier access to some widgets:
                self.expChannelOneView = self.ui.experimentDataPlots.ui.channelOneView
                self.expChannelTwoView = self.ui.experimentDataPlots.ui.channelTwoView
                self.ui.setSavePathButton.clicked.connect(self.set_path_function)
                # for data saving:
                self.DataList = DataArray()
                self.DataList.results.connect(self.DebugLog)
                self.loadEntriesFromConfig()
                pass
        
        def updateChannelsOsc(self):
                try:
                        signalChannelKey = self.ui.signalChannelOscBox.currentText()
                        responseChannelKey = self.ui.responseChannelOscBox.currentText()
                        # print(signalChannelKey, responseChannelKey, "sig & resp")
                        self.Osciloscope.responseChannel = self.Osciloscope._channels[responseChannelKey]
                        self.Osciloscope.signalChannel = self.Osciloscope._channels[signalChannelKey]
                        self.DebugMessage("OSC signalas - "+ self.Osciloscope.signalChannel+" ; atsakas : "+self.Osciloscope.responseChannel, 2500)
                except Exception as ex:
                        pass
                pass
        
        def saveRawExpData(self):
                try:
                        filename = self.ui.experimentFileNameEdit.text()
                        filepath = self._path
                        dateStamp = self.ui.dateEdit.text()
                        plotItem_one = self.expChannelOneView.plotItem
                        export = exporters.CSVExporter(plotItem_one)
                        export.export(filepath + "/" + filename+"_CH1_"+dateStamp)
                        plotItem_two = self.expChannelTwoView.plotItem
                        export = exporters.CSVExporter(plotItem_two)
                        export.export(filepath + "/" + filename+"_CH2_" + dateStamp)
                except Exception as ex:
                        self.DebugLog(tb.format_exc())
                        self.ExperimentInfo(str(ex))
                        pass
                pass

        def saveData(self):
                '''

                :return:
                '''
                try:
                        if self.ui.tabWidget.currentIndex() == 2:
                                fileNamePath = self._path+"/"+self.ui.experimentFileNameEdit.text()
                                self.DataList.write_all_lists(fileNamePath)
                                pass
                        elif self.ui.tabWidget.currentIndex() == 0:
                                self.RenewGeneratorFields()
                                additional_text = "_AMPL"+str(self.ui.voltageAmplitudeBox.value())+"_OFFS" +str( self.ui.voltageOffsetBox.value())+"_per"+str(self.ui.periodBox.value())
                                # additionl_text = self.ui.
                                fileNamePath = self._path + "/" + self.ui.experimentFileNameEdit.text()+str(self.ui.resistanceBox.value())+"kOhm"+additional_text
                                plotItem = self.ui.dataViewWidget.plotItem
                                export = exporters.CSVExporter(plotItem)
                                export.export(fileNamePath)
                        pass
                except Exception as ex:
                        self.ui.tabWidget.setCurrentIndex(3)
                        self.DebugLog("saveData fn error")
                        self.DebugLog(tb.format_exc())

        def set_path_function(self):
                path = QtWidgets.QFileDialog().getExistingDirectory(self, "Failo išsaugojimo vieta")
                if path is not None or len(path) > 0:
                        self._path = path
                        self.ui.path_label.setText(self._path)
                        self.ui.pathLabel.setText(self._path)
                        pass
                pass

        def saveToTXT_oscillograph_view_function(self):
                filename = self.ui.textForTXTName.text()
                plotItem = self.ui.dataViewWidget.plotItem
                export = exporters.CSVExporter(plotItem)
                export.export(self._path+"/"+filename)
                pass

        def ConnectToAllDevices(self):
                try:
                        self.connectOscilograph()
                        self.connectGenerator()
                        self.runInitGenerator()
                        self.ExperimentInfo(self.ui.connection_status_label.text())
                        self.ExperimentInfo(self.ui.idn_label_oscilograph.text())
                #         Ensure that we see experiment tab:
                        self.ui.tabWidget.setCurrentIndex(2)
                        self.ui.devicesTabWidget.setCurrentIndex(2)
                except Exception as ex:
                        self.DebugLog(tb.format_exc())
                        self.ui.tabWidget.setCurrentIndex(3)
                        pass
                pass

        def SetFullScreen(self):
                if self.isFullScreen():
                        self.showNormal()
                        pass
                else:
                        self.showFullScreen()
                pass

        def sendCMDintoOcilograph(self):
                cmd = self.ui.cmdBoxForOSC.currentText()
                try:
                        if "?" in cmd:
                                answer = self.Osciloscope.read(cmd)
                                try:
                                        ats = answer.decode()
                                        self.showTextInOsc("====CMD====")
                                        self.showTextInOsc(cmd)
                                        self.showTextInOsc("===ANSW===")
                                        self.showTextInOsc(ats)
                                except:
                                        self.showTextInOsc("====CMD====")
                                        self.showTextInOsc(cmd)
                                        self.showTextInOsc("===ANSW===")
                                        self.showTextInOsc(answer)
                                pass
                        else:
                                self.Osciloscope.write(cmd)
                        pass
                except Exception as ex:
                        self.DebugLog(tb.format_exc())
                        self.ui.tabWidget.setCurrentIndex(3)
                        pass
                pass

        def GetAllParameters(self):
                if self.ui.sweepAmplitudeRadioButton.isChecked():
                        start = self.ui.startAmplitudeSweepBox.value()
                        stop = self.ui.stopAmplitudeSweepBox.value()
                        step = self.ui.stepForAmplitudeSweepBox.value()
                        fixedOFF = self.ui.fixedOffsetBox.value()
                        time = self.ui.timeForAmplOffsSweepBox.value()
                        if self.ui.time_unit_mS.isChecked():
                                t_unit = "mS"
                        elif self.ui.time_unit_S.isChecked():
                                t_unit = "S"
                        else:
                                t_unit = "uS"
                        parameters = {'key': 1,
                                      'startV': start,
                                      'stopV': stop,
                                      'stepV': step,
                                      'fixedOFF': fixedOFF,
                                      'OFFtime': time,
                                      'timeU': t_unit}
                elif self.ui.sweepOffsetRadioButton.isChecked():
                        start = self.ui.startOffsetSweepBox.value()
                        stop = self.ui.stopOffsetSweepBox.value()
                        step = self.ui.stepForOffsetSweep.value()
                        fixedV = self.ui.fixedAmplitudeBox.value()
                        time = self.ui.timeForAmplOffsSweepBox.value()
                        if self.ui.time_unit_mS.isChecked():
                                t_unit = "mS"
                        elif self.ui.time_unit_S.isChecked():
                                t_unit = "S"
                        else:
                                t_unit = "uS"

                        parameters = {'key': 2,
                                      'startOFF': start,
                                      'stopOFF': stop,
                                      'stepOFF': step,
                                      'fixedV': fixedV,
                                      'OFFtime': time,
                                      'timeU': t_unit}
                elif self.ui.sweepTimeRadioButton.isChecked():
                        start = self.ui.startTimeSweepBox.value()
                        stop = self.ui.stopTimeSweepBox.value()
                        step = self.ui.stepForTimeSweepBox.value()
                        fixedV = self.ui.fixedAmplTimeSweepBox.value()
                        fixedOFF = self.ui.fixedOffsTimeSweepBox.value()
                        if self.ui.time_unit_mS_t.isChecked():
                                t_unit = "mS"
                        elif self.ui.time_unit_S_t.isChecked():
                                t_unit = "S"
                        else:
                                t_unit = "uS"
                        parameters = {'key': 3,
                                      'startT': start,
                                      'stopT': stop,
                                      'stepT': step,
                                      'fixedV': fixedV,
                                      'fixedOFF': fixedOFF,
                                      'timeU': t_unit}
                else:
                        parameters = None
                return parameters
                pass


        def SetSweepFunctions(self):
                # we need always check if we have a proper status of generator:
                try:
                        self.RenewGeneratorFields()
                        SweepButtonsFunctionality(self.ui)
                        pass
                except Exception as ex:
                        self.DebugLog(tb.format_exc())
                        self.ui.tabWidget.setCurrentIndex(3)
                        #  we will continue even if renew function fails - we need this for debugging reasons
                        SweepButtonsFunctionality(self.ui)
                        pass
                pass

        def loadEntriesFromConfig(self):
                # TODO implement!
                configLoader = Configuration("Configs/Entries.ini")
                dev_dict = configLoader.USBTMCDevicesLoader()
                # trigger device search:
                self.scan_for_all_USBTMC_devices()
                for key in dev_dict:
                        if "gen" in key.lower():
                                index = self.ui.comboBox_for_generator.findText(dev_dict[key])
                                if index != -1:
                                        self.ui.comboBox_for_generator.setCurrentIndex(index)
                                else:
                                        pass
                                pass
                        elif "osc" in key.lower():
                                index = self.ui.comboBox_for_oscillograph.findText(dev_dict[key])
                                if index != -1:
                                        self.ui.comboBox_for_oscillograph.setCurrentIndex(index)
                                else:
                                        pass
                                pass
                        else:
                                pass
                        pass
                # TODO one
                configLoader.ConfigTCPIPLoader(self.ui.tableWithTCPIPDevices)
                path = configLoader.get_save_path()
                self._path = path
                print(path, "path loaded")
                self.ui.path_label.setText(self._path)
                pass


        def saveEntriesToConfig(self):
                # TODO implement
                self.DebugMessage("Not implemented yet!")
                pass

        def RenewGeneratorFields(self):
                frequency = self.Generator.GetFrequency(self.Generator.CH1)
                period = self.Generator.GetPeriod(self.Generator.CH1)
                amplitude = self.Generator.GetAmplitude(self.Generator.CH1)
                trigger_interval = self.Generator.GetTriggerInterval()
                offset = self.Generator.GetNormalizedOffset(self.Generator.CH1)
                # Need to fix units, aka μS, mS, S ...
                # Print all :
                # print("FREQ", frequency, "PERIOD", period, "AMPL", amplitude, "TRIG INT", trigger_interval, "Norm. OFFS", offset)
                self.ui.voltageOffsetBox.setValue(float(offset))
                self.ui.voltageAmplitudeBox.setValue(float(amplitude))
                # We need appropriate values and their units
                period_floored, unit_period = getNumberSIprefix(float(period))
                trigger_interval_floored, unit_trigger = getNumberSIprefix(float(trigger_interval))
                freq_floored, unit_freq = getNumberSIprefix(float(frequency))
                self.ui.periodBox.setValue(float(period_floored))
                self.ui.triggerIntervalBox.setValue(float(trigger_interval_floored))
                self.setCorrectUnits(unit_freq, unit_period, unit_trigger)
                # ============================
                #  TODO fix and correctly set units for freq trigg and period!
                self.DebugGenerator("========================")
                self.DebugGenerator("freq", frequency, "trigg", trigger_interval, "period", period)
                self.DebugGenerator("freq", freq_floored, unit_freq, "trigg", trigger_interval_floored, unit_trigger, "period", period_floored, unit_period)
                self.DebugGenerator("========================")
                pass

        def setCorrectUnits(self, freq_unit, period_unit, trigger_unit):
                if "μ" in period_unit:
                        self.ui.periodRadioButton_uS.setChecked(True)
                elif "m" in period_unit:
                        self.ui.periodRadioButton_mS.setChecked(True)
                else:
                        self.ui.periodradioButton_S.setChecked(True)
                        pass
                if "μ" in trigger_unit:
                        self.ui.triggerInterval_uS.setChecked(True)
                elif "m" in trigger_unit:
                        self.ui.triggerInterval_mS.setChecked(True)
                else:
                        self.ui.triggerInterval_S.setChecked(True)
                        pass


        def StartExperimentLoop(self):
                try:
                        # TODO it looks like the right way how I need to implement this stuff:
                        if "Pradėta" in self.ui.startExperimentButton.text():
                                self.DebugMessage("Thread is already running")
                                self.DebugMessage("Trying to stop it")
                                self._worker.stop()
                                pass
                        elif "Pradėti" in self.ui.startExperimentButton.text():
                                if len(self._threads) > 0:
                                        # self._threads = []
                                        pass
                                # get all parameters:
                                parameters_tuple = self.GetAllParameters()
                                #
                                self.expChannelOneView.clear()
                                self.expChannelTwoView.clear()
                                self.ui.startExperimentButton.setText("Pradėta [Sustabdyti]")
                                self._thread = QThread()
                                self._thread.setObjectName("WLoop")
                                self._worker = LoopWorker(self.Generator, self.Osciloscope,  **parameters_tuple)
                                self._worker.moveToThread(self._thread)
                                self._worker.results.connect(self.draw_exp_data)
                                self._worker.final.connect(self.WorkerEnded)
                                self._worker.errors.connect(self.ErrorHasBeenGot)
                                self._worker.progress.connect(self.ExperimentInfo)
                                self._thread.started.connect(self._worker.run)
                                self._thread.start()
                                pass
                        else:
                                self.DebugMessage("Some shit")
                except Exception as ex:
                        self.DebugLog("Problems with starting of threads")
                        self.DebugLog(tb.format_exc())
                        self.ui.tabWidget.setCurrentIndex(3)
                        pass

        def ErrorHasBeenGot(self, *args):
                self.DebugLog(str(args[0]))
                self.DebugLog(args[1])
                pass

        def WorkerEnded(self, i:int):
                self.ui.startExperimentButton.setText("Pradėti")
                pass

        def SetTriggerInterval_gen(self):
                self.checkStateOfRadioButtons()
                interval = self.ui.triggerIntervalBox.value()
                self.Generator.SetTriggerInterval(interval, self.TriggerIntervalUnit)
                int=self.Generator.GetTriggerInterval()
                self.DebugGenerator("Intervalas", int)
                pass

        def setPeriod_generator(self):
                self.checkStateOfRadioButtons()
                period = self.ui.periodBox.value()
                self.Generator.SetPeriod(self.Generator.CH1, period, self.PeriodUnit, self.PeriodPower)
                # Test of settled parameters:
                period = self.Generator.GetPeriod(self.Generator.CH1)
                self.DebugGenerator("Periodas", period)
                freq = self.Generator.GetFrequency(self.Generator.CH1)
                self.DebugGenerator("Dažnis", freq)
                pass

        def setOffset_generator(self):
                offset = self.ui.voltageOffsetBox.value()
                amplitude = self.ui.voltageAmplitudeBox.value()
                self.Generator.SetNormalizedOffset(self.Generator.CH1, offset, amplitude)
                # Test:
                off = self.Generator.GetOffset(self.Generator.CH1)
                self.DebugGenerator("Offset'as", off)
                pass

        def sendCustomGenCmd(self):
                cmd = self.ui.cmd_custom_for_generator.currentText()
                self.DebugMessage(cmd, 3000)
                if("?" in cmd):
                        ats = self.Generator.Ask(cmd)
                        self.DebugGenerator(cmd, ats)
                else:
                        self.Generator.Write(cmd)
                pass



        def setGeneratorsAmplitude(self):
                Amplitude = self.ui.voltageAmplitudeBox.value()
                self.DebugMessage(str(Amplitude), 2000)
                self.Generator.SetAmplitude(self.Generator.CH1, Amplitude)

        def checkStateOfRadioButtons(self):
                if(self.ui.periodRadioButton_uS.isChecked()):
                        self.PeriodUnit = "uS"
                        self.PeriodPower = 1E-6
                        pass
                elif(self.ui.periodRadioButton_mS.isChecked()):
                        self.PeriodUnit = "mS"
                        self.PeriodPower = 1e-3
                        pass
                elif(self.ui.periodradioButton_S.isChecked()):
                        self.PeriodUnit = "S"
                        self.PeriodPower = 1e0
                        pass
                else:
                        self.PeriodUnit = "mS"
                        self.PeriodPower = 1e-3
                        self.DebugMessage("mS liko, nekeista", 1000)
                        pass
                if(self.ui.triggerInterval_mS.isChecked()):
                        self.TriggerIntervalUnit = "mS"
                        self.TriggerIntervalPower = 1e-3
                        pass
                elif(self.ui.triggerInterval_uS.isChecked()):
                        self.TriggerIntervalUnit = "uS"
                        self.TriggerIntervalPower = 1e-6
                        pass
                elif(self.ui.triggerInterval_S.isChecked()):
                        self.TriggerIntervalUnit = "S"
                        self.TriggerIntervalPower = 1e0
                        pass
                else:
                        self.TriggerIntervalUnit = "mS"
                        self.TriggerIntervalPower = 1e-3
                        pass
                pass

        def StateChanged(self, int):
                # TODO threading?
                self.DebugMessage("State changed, got parameter "+str(int), 1000)
                if (int == 0):
                        # Unchecked
                        # We can not terminate QRunnable, at least not now. This
                        # functionality is not supported yet.
                        pass
                elif (int == 2):
                        # checked state
                        # TODO we need normal signal handling
                        if self.ThreadPool.activeThreadCount()<=0:
                                time = self.ui.secondsToWait.value()
                                count = self.ui.noMoreThanTimes_oscilograph.value()
                                worker = RigolBackGround_scanner(self.Osciloscope.get_data_points_from_channel, self.Osciloscope.signalChannel, time, count)
                                worker.signals.result.connect(self.DrawOscilogramm)
                                worker.signals.error.connect(self.DebugLog)
                                # worker.signals.progress.connect(self.ExperimentInfo)
                                worker.signals.finished.connect(self.FinnishedQRunnable)
                                self.ThreadPool.start(worker)
                        else:
                                print(self.ThreadPool.activeThreadCount(), "Already something's running")
                        pass
                else:
                        self.DebugMessage("Shit happened "+str(int), 1000)
                        pass
                # self.DebugMessage("")

        def ExperimentInfo(self, string):
                self.ui.experimentPlainLog.appendPlainText(string)
                pass

        def FinnishedQRunnable(self):
                self.ui.useRegularUpdateBox.setChecked(False)
                pass

        def SetupWindow(self):
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("Icons/comport.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setWindowIcon(icon)
                self.dataCurveOne.setPen((200, 200, 100))
                self.dataCurveTwo.setPen((100, 200, 255))
                SetupWindow(self.ui) # maybe it works?
                pass

        def getDatafromBothChannels_button_clicked(self):
                self.getVoltsFromChannel(self.Osciloscope.signalChannel, self.dataCurveOne, self.ui.dataViewWidget)
                self.getVoltsFromChannel(self.Osciloscope.responseChannel, self.dataCurveTwo, self.ui.dataViewWidget)
                pass

        def getVoltsFromCH2_button_clicked(self):
                self.getVoltsFromChannel(self.Osciloscope.responseChannel, self.dataCurveTwo, self.ui.dataViewWidget)
                pass

        def getVoltsFromChannel(self, CH:str, dataCurve, graph:pG.PlotWidget):
                data_from_channel, time_array, time_unit = self.Osciloscope.get_data_points_from_channel(CH)
                print("time unit", time_unit)
                graph.setLabel('bottom', 'Time', units=time_unit)
                graph.setLabel('left', 'Voltage', units='V')
                dataCurve.setData(time_array, data_from_channel)
                self.DebugMessage("Working on it ...", 1000)
                pass

        def draw_exp_data(self, CH1, CH2, time, time_unit, m_dict):
                try:
                        R = self.ui.resistanceBox.value()
                        S = self.ui.areaBox.value()
                        self.expChannelOneView.setLabel('bottom', 'Time', units=time_unit)
                        self.expChannelOneView.setLabel('left', 'Voltage', units='V')
                        self.expChannelTwoView.setLabel('bottom', 'Time', units=time_unit)
                        self.expChannelTwoView.setLabel('left', 'Voltage', units='V')
                        expCOne = self.expChannelOneView.plot()
                        expCTwo = self.expChannelTwoView.plot()
                        rOne = random.randint(100, 255)
                        gOne = random.randint(100, 255)
                        bOne = random.randint(100, 255)
                        rTwo = random.randint(150, 255)
                        gTwo = random.randint(150, 255)
                        bTwo = random.randint(150, 255)
                        expCOne.setPen((rOne, gOne, bOne))
                        expCTwo.setPen((rTwo, gTwo, bTwo))
                        expCOne.setData(time, CH1)
                        expCTwo.setData(time, CH2)
                        self.DebugMessage("Working on it ...", 1000)
                        if self.ui.enableAutoSaveBox.isChecked():
                                amplitude = str(m_dict["AMPL"])
                                offset = str(m_dict["OFFS"])
                                period= str(m_dict["PERIOD"])
                                time_unit = str(m_dict["TIMEU"])
                                measurement_params = "AMPL: "+amplitude + " V | OFFS: "+offset+" V | PERIOD: "+period+" "+time_unit
                                fName = self._path+"/"+str(self.ui.experimentFileNameEdit.text()+"_ampl"+amplitude+"_off"+offset+"_int"+period+".csv")
                                mObject = MeasurementData(fName)
                                mObject.results.connect(self.DebugLog)
                                mObject.set_data_array(R, S, time, time_unit, CH1, CH2, measurement_params)
                                mObject.write_to_file()
                                self.ExperimentInfo("Saved to "+fName)
                                pass
                        else:
                                amplitude = str(m_dict["AMPL"])
                                offset = str(m_dict["OFFS"])
                                period = str(m_dict["PERIOD"])
                                time_unit = str(m_dict["TIMEU"])
                                measurement_params = "AMPL: " + amplitude + " V | OFFS: " + offset + " V | PERIOD: " + period + " " + time_unit
                                self.DataList.append(R, S, TIME=time, CHAN1=CH1, CHAN2=CH2, MPARAMS=measurement_params,TIMEU=time_unit, NAME="_ampl"+amplitude+"_off"+offset+"_int"+period)
                                pass
                except Exception as ex:
                        self.DebugLog("================")
                        self.DebugLog(tb.format_exc())
                        self.ui.tabWidget.setCurrentIndex(3)


        def DrawOscilogramm(self, result):
                data = result[0]
                time = result[1]
                timeUnit = result[2]
                #
                self.dataCurveOne.setData(time, data)
                pass

        def connectOscilograph(self):
                try:
                        self.Osciloscope = GetOscilograph(self.ui, self.DevicesUSBTMC)
                        msg = self.Osciloscope.get_name()
                        self.ui.idn_label_oscilograph.setText((msg)[0:10])
                        self.DebugMessage("IDN: " + msg, 1000)
                        self.initOscilograph()
                        self.ui.connectToOscilograph_button.setText("Prisijungta")
                        pass
                except Exception as ex:
                        self.DebugLog("connectOscilograph fn error")
                        self.DebugLog(tb.format_exc())
                        self.ui.tabWidget.setCurrentIndex(3)
                        pass

        def initOscilograph(self):
                # osc_conf = Configuration("Configs/RigolDS1101E.ini")
                list_cmds = self.Osciloscope.get_init_conf()
                self.DebugLog("===Osciloscope init file ===")
                self.DebugLog(list_cmds)
                self.ui.plainConfigOscilograph.setPlainText(list_cmds)
                cmds = getTextLinesFromQTextEditField(self.ui.plainConfigOscilograph)
                # It seems working until ths point:
                for i in cmds:
                        self.Osciloscope.write(i)
                        self.ui.cmdBoxForOSC.addItem(str(i))
                        time.sleep(0.25)
                self.Osciloscope.unlock_key()
                # fill all additional information:
                self.fillChannelCombos()
                self.updateChannelsOsc()
                pass
        
        def fillChannelCombos(self):
                channels_count = len(self.Osciloscope._channels)
                for i in range(1, channels_count+1):
                        self.ui.signalChannelOscBox.addItem(str(i))
                        self.ui.responseChannelOscBox.addItem(str(i))
                        pass
                self.ui.responseChannelOscBox.setCurrentIndex(1) # usually oscilloscopes have two channels, safe to set it.
                pass
        
        def showTextInOsc(self, text):
                self.ui.plainConfigOscilograph.appendPlainText(str(text))

        def getVoltsFromCH1_button_clicked(self):
                self.getVoltsFromChannel(self.Osciloscope.signalChannel, self.dataCurveOne, self.ui.dataViewWidget)
                pass
        
        
        def changeOutputCH1(self):
                if(self.ui.InputOutputCH1Button.isChecked()):
                        # self.Generator.ask("C1:OUTP ON")
                        self.Generator.EnableOutput(self.Generator.CH1, ON)
                        self.DebugMessage("CH1 ON", 1000)
                else:
                        # self.Generator.ask("C1:OUTP OFF")
                        self.Generator.EnableOutput(self.Generator.CH1, OFF)
                        self.DebugMessage("CH1 OFF", 1000)
                pass

        def changeOutputCH2(self):
                if (self.ui.InputOutputCH2Button.isChecked()):
                        # self.Generator.ask("C2:OUTP ON")
                        self.Generator.EnableOutput(self.Generator.CH2, ON)
                        self.DebugMessage("CH2 ON", 1000)
                else:
                        # self.Generator.ask("C2:OUTP OFF")
                        self.Generator.EnableOutput(self.Generator.CH2, OFF)
                        self.DebugMessage("CH2 OFF", 1000)
                pass

        def runInitGenerator(self):
                '''
                Initialization of generator, populate QComboBox Items also.

                :return:
                '''
                listOfCommands = getTextLinesFromQTextEditField(self.ui.initialConfigurationForGenerator)
                for i in listOfCommands:
                        self.Generator.Write(str(i))
                        self.ui.cmd_custom_for_generator.addItem(str(i))
                        time.sleep(0.1)
                        pass
                self.RenewGeneratorFields()
                pass




        def connectGenerator(self):
                self.Generator = GetGenerator(self.ui, self.DevicesUSBTMC)
                self.Generator.errors.connect(self.DebugLog)
                name = self.Generator.GetIDN()
                self.DebugLog("Testas prisijungimo")
                self.ui.connection_status_label.setText(name[0:15])
                # #  populate init commands from file:
                # # myConf = Configuration("Configs/Siglent.ini")
                lines = self.Generator.GetInitConfiguration()
                # self.DebugLog(lines)
                self.ui.initialConfigurationForGenerator.setPlainText(lines)
                pass


        def removeSelectedRow(self):
                index = self.ui.tableWithTCPIPDevices.currentRow()
                self.ui.tableWithTCPIPDevices.removeRow(index)

        def getIDN_from_selected_table_device(self):
                index = self.ui.tableWithTCPIPDevices.currentRow()
                ip_string = self.ui.tableWithTCPIPDevices.item(index,0).text()
                self.DebugLog(ip_string)
                IDN = self.get_IDN_from_IP(ip_string)
                self.DebugLog(IDN)
                item = QtWidgets.QTableWidgetItem(IDN)
                self.ui.tableWithTCPIPDevices.setItem(index,3, item)
                pass


        def setupTable(self):
                self.ui.tableWithTCPIPDevices.setColumnCount(5)
                self.ui.tableWithTCPIPDevices.setHorizontalHeaderLabels(["TCP/IP adresas","Gen/Osc?", "Naudoti?", "*IDN?", "Nr."])
                self.ui.tableWithTCPIPDevices.setColumnWidth(0, 160)
                self.ui.tableWithTCPIPDevices.setColumnWidth(1, 160)
                pass


        def addRowIntoTable(self):
                listOfDevices=["Generatorius", "Oscilografas"]
                i = self.ui.tableWithTCPIPDevices.rowCount()
                if i is not None:
                        self.ui.tableWithTCPIPDevices.setRowCount(i+1)
                        self.ui.tableWithTCPIPDevices.setCellWidget(i,1,QtWidgets.QComboBox())
                        self.ui.tableWithTCPIPDevices.cellWidget(i,1).addItems(listOfDevices)
                        self.ui.tableWithTCPIPDevices.setCellWidget(i,2, QtWidgets.QCheckBox())
                        self.ui.tableWithTCPIPDevices.cellWidget(i,2).setChecked(False)
                        cell = QtWidgets.QTableWidgetItem()
                        cell.setText(str(i))
                        self.ui.tableWithTCPIPDevices.setItem(i, 4, cell)
                        self.ui.tableWithTCPIPDevices.selectRow(i)
                else:
                        self.ui.tableWithTCPIPDevices.setRowCount(1)
                        self.ui.tableWithTCPIPDevices.setCellWidget(1, 1, QtWidgets.QComboBox())
                        self.ui.tableWithTCPIPDevices.cellWidget(1, 1).addItems(listOfDevices)
                        self.ui.tableWithTCPIPDevices.setCellWidget(1, 2, QtWidgets.QCheckBox())
                        self.ui.tableWithTCPIPDevices.cellWidget(1, 2).setChecked(False)
                        cell = QtWidgets.QTableWidgetItem()
                        cell.setText(str(1))
                        self.ui.tableWithTCPIPDevices.setItem(1, 4, cell)
                        self.ui.tableWithTCPIPDevices.selectRow(1)
                pass

        def closeFn(self):
                try:
                        if self.Generator is not None:
                                # self.Generator.ask("*RST")
                                # Nereikia čia reset'o daryti.
                                self.Generator.Close()
                        if self.Osciloscope is not None:
                                self.Osciloscope.unlock_key()
                                self.Osciloscope.close()
                        # print("Debug: exit")
                        # čia turi būti funkcija, atsijungianti nuo prietaisų ir juos nustatanti į defaul režimą;
                        sys.exit(0)
                        pass
                except Exception as ex:
                        print(ex)
                        sys.exit(0)
                        pass
                pass

        def clearTextInIfoFiel(self):
                self.ui.advancedTextEditForErrors.clear()
                pass


        def unusedFunction(self):
                self.ui.statusbar.showMessage("Ti gi sakiau, neveikia!")
                pass


        def scan_for_all_USBTMC_devices(self):
                #  clear at first:
                self.DevicesUSBTMC.clear()
                self.ui.list_of_devices_comboBox.clear()
                self.ui.comboBox_for_oscillograph.clear()
                self.ui.comboBox_for_generator.clear()
                mypath = "/dev"
                for f in os.listdir(mypath):
                        if f.startswith('usbtmc'):
                                try:
                                        self.DebugLog(mypath+"/"+f)
                                        dvs = SimpleInstrument("/dev/" + f)
                                        answer = dvs.getName()
                                        self.DebugLog(str(answer.decode("utf-8")).replace("\n",""))
                                        # put this device name into dictionary, to use them later
                                        self.DevicesUSBTMC["/dev/"+f] = str(answer.decode("utf-8")).replace("\n","")
                                        self.fill_all_boxes_with_devices(mypath+"/"+f)
                                        if "rigol".lower() in str(answer.decode("utf-8")).lower():
                                                dvs.write(":KEY:FORC")
                                                pass
                                        # dvs.reset() # no reset!
                                        dvs.close()
                                except Exception as e:
                                        self.DebugLog("scan_for_all_USBTMC_devices fn error")
                                        self.DebugLog(str(e))
                                        self.DebugMessage("Problemos su USBTMC prietaisais?", 2500)
                                        self.ui.tabWidget.setCurrentIndex(3)
                                        pass
                # nothing to do
                # last entry is related to the ability to unset any device:
                self.ui.comboBox_for_oscillograph.addItem("[Nėra]")
                self.ui.comboBox_for_generator.addItem("[Nėra]")
                pass

        def fill_all_boxes_with_devices(self, item):
                answer= self.DevicesUSBTMC[item]
                # add into comboboxes:
                self.ui.list_of_devices_comboBox.addItem(answer)
                self.ui.comboBox_for_oscillograph.addItem(answer)
                self.ui.comboBox_for_generator.addItem(answer)
                pass

        def DebugLog(self, error_text, error_status=0):
                if(error_status==0):
                        self.ui.advancedTextEditForErrors.append(error_text)
                        pass
                pass

        def DebugMessage(self, msg, time=1000):
                self.ui.statusbar.showMessage(msg, time)
                pass

        def DebugGenerator(self, msg, txt=None):
                if txt is not None:
                        self.ui.answersFromGeneratorTextBox.appendPlainText(str(msg)+" :: "+str(txt)+" |")
                else:
                        self.ui.answersFromGeneratorTextBox.appendPlainText(str(msg) + " |")

                pass

        def DebugGenerator(self, *args):
                l = ""
                for i in args:
                        l = l + str(i)+" "
                        pass
                self.ui.answersFromGeneratorTextBox.appendPlainText(l)
                pass

        def get_IDN_from_IP(self, ip_string):
                instr = vxi11.Instrument(ip_string)
                answer = instr.ask("*IDN?")
                instr.close() # always close a device.
                return answer

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        # sys.argv always is equal at least to one, script itself.
        if len(sys.argv) > 1:
                if sys.argv[1] == "--fullscreen":
                        window.showFullScreen()
                else:
                        pass
        else:
                window.show() # just show a window()
        sys.exit(app.exec_())
