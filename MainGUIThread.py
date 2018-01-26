#!/usr/bin/python3
from PyQt5 import QtCore, QtWidgets, QtGui
from UIfiles.GUIThread import Ui_MainGuiWindow

import sys, os
from USBTMC_Devices import *
from GetInfoAboutDevices import *
from ConfigParser import *
import vxi11
import random
import pyqtgraph as pG

#

from Generators.SiglentGenerator import *
from Generators.TektronixGenerator import *
from MainExperimentLoopThread import *
from DummyFiles.DummyFunctions import *
from Units.UnitCheck import *
from UIfiles.UISetupFunctions import *
# Very global dictionary for all devices?
# prettier graphs:
pG.setConfigOptions(antialias=True)
# very global variables:
ON = "ON"
OFF = "OFF"
from ThreadedRigolreading import *
class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super(MainWindow, self).__init__()
                self.ui = Ui_MainGuiWindow()
                self.ui.setupUi(self)
                #Normally this is all to be done in order to show a window
                self.ThreadPool = QThreadPool() # because of threading?
                self._threads = []
                # plots:
                self._plots = []
                #declare global self.dictionary:
                self.Devices_dict={} # for USBTMC
                self.Devices_TCP={} # for TCP/IP devices
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
                self.ekspCurveOne = self.ui.experimentDataViewPlot.plot()
                self.ekspCurveTwo = self.ui.experimentDataViewPlot.plot()
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
                # Main loop:
                self.ui.startExperimentButton.clicked.connect(self.StartExperimentLoop)
                # Configuration saving and loading:
                self.ui.saveEntriesButton.clicked.connect(self.saveEntriesToConfig)
                self.ui.loadEntriesButton.clicked.connect(self.loadEntriesFromConfig)
                self.ui.sweepAmplitudeRadioButton.clicked.connect(self.SetSweepFunctions)
                self.ui.sweepOffsetRadioButton.clicked.connect(self.SetSweepFunctions)
                self.ui.sweepTimeRadioButton.clicked.connect(self.SetSweepFunctions)
                pass

        def GetAllParameters(self):
                if self.ui.sweepAmplitudeRadioButton.isChecked():
                        start = self.ui.startAmplitudeSweepBox.value()
                        stop = self.ui.stopAmplitudeSweepBox.value()
                        step = self.ui.stepForAmplitudeSweepBox.value()
                        fixedOFF = self.ui.fixedOffsetBox.value()
                        time = self.ui.timeForAmplOffsSweepBox.value()
                        parameters = {'key': 1,
                                      'startV': start,
                                      'stopV': stop,
                                      'stepV': step,
                                      'fixedOFF': fixedOFF,
                                      'OFFtime': time}
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
                else:
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
                return parameters
                pass

        
        def SetSweepFunctions(self):
                # we need always check if we have a proper status of generator:
                try:
                        self.RenewGeneratorFields()
                        SweepButtonsFunctionality(self.ui)
                        pass
                except Exception as ex:
                        self.DebugLog(str(ex))
                        #  we will continue even if renew function fails - we need this for debugging reasons
                        SweepButtonsFunctionality(self.ui)
                        pass
                pass

        def loadEntriesFromConfig(self):
                # TODO implement!
                configLoader = Configuration("Configs/Entries.ini")
                configLoader.USBTMCDevicesLoader(self.ui)
                self.DebugMessage("Not implemented yet!")
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
                offset = self.Generator.GetOffset(self.Generator.CH1)
                # Need to fix units, aka μS, mS, S ...
                # Print all :
                print("FREQ", frequency, "PERIOD", period, "AMPL", amplitude, "TRIG INT", trigger_interval, "OFFS", offset)
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
                # TODO it looks like the right way how I need to implement this stuff:
                if "Pradėta" in self.ui.startExperimentButton.text():
                        self.DebugMessage("Thread is already running")
                        pass
                elif "Pradėti" in self.ui.startExperimentButton.text():
                        if len(self._threads) > 0:
                                self._threads = []
                                pass
                        # get all parameters:
                        parameters_tuple = self.GetAllParameters()
                        #
                        thread = QThread()
                        thread.setObjectName("WLoop")
                        workerLoop = LoopWorker(self.Generator, self.Osciloscope, **parameters_tuple)
                        print(thread.objectName())
                        self._threads.append((thread, workerLoop))
                        workerLoop.moveToThread(thread)
                        workerLoop.results.connect(self.drawexp)
                        workerLoop.final.connect(self.WorkerEnded)
                        workerLoop.errors.connect(self.ErrorHasBeenGot)
                        thread.started.connect(workerLoop.run)
                        thread.start()
                        self.ui.startExperimentButton.setText("Pradėta")
                        pass
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
                self.Generator.SetOffset(self.Generator.CH1, offset)
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
                                worker = RigolBackGround_scanner(self.Osciloscope.get_data_points_from_channel, "CHAN1", time, count)
                                worker.signals.result.connect(self.DrawOscilogramm)
                                worker.signals.error.connect(self.DebugLog)
                                worker.signals.finished.connect(self.FinnishedQRunnable)
                                self.ThreadPool.start(worker)
                        else:
                                print(self.ThreadPool.activeThreadCount(), "Already something's running")
                        pass
                else:
                        self.DebugMessage("Shit happened "+str(int), 1000)
                        pass
                # self.DebugMessage("")
                
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
                self.getVoltsFromChannel("CHAN1", self.dataCurveOne, self.ui.dataViewWidget)
                self.getVoltsFromChannel("CHAN2", self.dataCurveTwo, self.ui.dataViewWidget)
                pass

        def getVoltsFromCH2_button_clicked(self):
                self.getVoltsFromChannel("CHAN2", self.dataCurveTwo, self.ui.dataViewWidget)
                pass
        
        # def ekspMatavimas_clicked(self):
        #         self.getVoltsFromChannel(self.Osciloscope.CH1, self.ekspCurveOne, self.ui.experimentDataViewPlot)
        #         self.getVoltsFromChannel(self.Osciloscope.CH2, self.ekspCurveTwo, self.ui.experimentDataViewPlot)
        #         pass

        def getVoltsFromChannel(self, CH:str, dataCurve, graph:pG.PlotWidget):
                data_from_channel, time_array, time_unit = self.Osciloscope.get_data_points_from_channel(CH)
                graph.setLabel('bottom', 'Time', units=time_unit)
                graph.setLabel('left', 'Voltage', units='V')
                dataCurve.setData(time_array, data_from_channel)
                self.DebugMessage("Working on it ...", 1000)
                pass
        
        def drawexp(self, CH1, CH2, time, time_unit):
                self.ui.experimentDataViewPlot.setLabel('bottom', 'Time', units=time_unit)
                self.ui.experimentDataViewPlot.setLabel('left', 'Voltage', units='V')
                expCOne = self.ui.experimentDataViewPlot.plot()
                expCTwo = self.ui.experimentDataViewPlot.plot()
                # self.dataCurveOne.setPen((200, 200, 100))
                # self.dataCurveTwo.setPen((100, 200, 255))
                rOne = random.randint(100, 255)
                gOne = random.randint(100, 255)
                bOne = random.randint(100, 255)
                rTwo = random.randint(100, 255)
                gTwo = random.randint(100, 255)
                bTwo = random.randint(100, 255)
                expCOne.setPen((rOne, gOne, bOne))
                expCTwo.setPen((rTwo, gTwo, bTwo))
                self._plots.append((expCOne, expCTwo))
                # self.ekspCurveOne.setData(time, CH1)
                # self.ekspCurveTwo.setData(time, CH2)
                expCOne.setData(time, CH1)
                # expCTwo.setData(time, CH2)
                self.DebugMessage("Working on it ...", 1000)
                
        
        def DrawOscilogramm(self, result):
                data = result[0]
                time = result[1]
                timeUnit = result[2]
                #
                self.dataCurveOne.setData(time, data)
                pass
        
        def connectOscilograph(self):
                try:
                        connected_devices = getDevicesFromComboBoxes(self.ui.comboBox_for_generator, self.ui.comboBox_for_oscillograph, self.Devices_dict)
                        self.Osciloscope = RigolDS1000SeriesScope(connected_devices[3])
                        msg = self.Osciloscope.get_name()
                        self.ui.idn_label_oscilograph.setText((msg.decode())[0:10])
                        self.DebugMessage("IDN: "+msg.decode(), 1000)
                        self.initOscilograph() # do not forget to call this function
                except Exception as ex:
                        self.DebugLog("===Problemos su oscilografu===")
                        self.DebugLog(str(ex))
                        pass
                pass

        def initOscilograph(self):
                osc_conf = Configuration("Configs/RigolDS1101E.ini")
                list_cmds = osc_conf.readDefaultInitCommands("RIGOL INIT SETUP","InitRigol")
                self.DebugLog("===Rigol init file===")
                self.DebugLog(list_cmds)
                self.ui.plainConfigOscilograph.setPlainText(list_cmds)
                cmds = getTextLinesFromQTextEditField(self.ui.plainConfigOscilograph)
                # It seems working until ths point:
                for i in cmds:
                        self.Osciloscope.write(i)
                        time.sleep(0.25)
                self.Osciloscope.unlock_key()
                pass

        def getVoltsFromCH1_button_clicked(self):
                self.getVoltsFromChannel("CHAN1", self.dataCurveOne)
                pass
        # def setupPlotWidget(self):
        #         '''
        #         Draw correct axes and so on:
        #
        #         :return:
        #         '''
        #         self.ui.dataViewWidget.plotItem.showGrid(True, True, 1.0)
        #         self.ui.experimentDataViewPlot.plotItem.showGrid(True, True, 1.0)
        #         pass
                
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
                # at first, we should get an generator from our tables/comboBox:
                # second, we have to check USBTMC devices for a generator
                Devices_from_TCP_table=getDevicesFromTable(self.ui.tableWithTCPIPDevices)
                for key in Devices_from_TCP_table.keys():
                        self.DebugLog(str(key))
                        self.DebugLog(Devices_from_TCP_table[key])
                Gen = getDevicePathWithRoleFromList("Generatorius", Devices_from_TCP_table)
                self.DebugLog(Gen)
                # test IDN again:
                idn = vxi11.Instrument(Gen)
                name = idn.ask("*IDN?")
                idn.close() # close device, we will initialize it a little bit later;
                if "Siglent".lower() in name.lower():
                        self.Generator = SiglentGenerator_TCP(Gen)
                        self.Generator.IDN = name
                        self.DebugLog("Siglent rastas")
                        pass
                elif "Tektronix".lower() in name.lower():
                        self.Generator = TektronixGenerator_TCP(Gen)
                        self.Generator.IDN = name
                        self.DebugLog("Tektronix rastas")
                        pass
                else:
                        self.DebugMessage("Unknown device", 2500)
                        pass
                self.DebugLog("Testas prisijungimo")
                self.ui.connection_status_label.setText(name[0:15])
                #  populate init commands from file:
                # myConf = Configuration("Configs/Siglent.ini")
                lines = self.Generator.GetInitConfiguration()
                self.DebugLog(lines)
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
                if self.Generator is not None:
                        # self.Generator.ask("*RST")
                        # Nereikia čia reset'o daryti.
                        self.Generator.Close()
                if self.Osciloscope is not None:
                        self.Osciloscope.close()
                # print("Debug: exit")
                # čia turi būti funkcija, atsijungianti nuo prietaisų ir juos nustatanti į defaul režimą;
                sys.exit(0)
                pass
        
        def clearTextInIfoFiel(self):
                self.ui.advancedTextEditForErrors.clear()
                pass
        
        
        def unusedFunction(self):
                self.ui.statusbar.showMessage("Ti gi sakiau, neveikia!")
                pass
        
        
        def scan_for_all_USBTMC_devices(self):
                #  clear at first:
                self.Devices_dict.clear()
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
                                        self.Devices_dict["/dev/"+f] = str(answer.decode("utf-8")).replace("\n","")
                                        self.fill_all_boxes_with_devices(mypath+"/"+f)
                                        if "rigol".lower() in str(answer.decode("utf-8")).lower():
                                                dvs.write(":KEY:FORC")
                                                pass
                                        # dvs.reset() # no reset!
                                        dvs.close()
                                except Exception as e:
                                        self.DebugLog(str(e))
                                        self.DebugMessage("Problemos su USBTMC prietaisais?", 2500)
                                        pass
                # nothing to do
                # last entry is related to the ability to unset any device:
                self.ui.comboBox_for_oscillograph.addItem("[Nėra]")
                self.ui.comboBox_for_generator.addItem("[Nėra]")
                pass
        
        def fill_all_boxes_with_devices(self, item):
                answer= self.Devices_dict[item]
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
        window.show()
        sys.exit(app.exec_())