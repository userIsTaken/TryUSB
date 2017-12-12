#!/usr/bin/python3
from PyQt5 import QtCore, QtWidgets, QtGui
from UIfiles.GUIThread import Ui_MainGuiWindow

import sys, os
from USBTMC_Devices import *
from GetInfoAboutDevices import *
from ConfigParser import *
import vxi11
import pyqtgraph as pG

#

from Generators.SiglentGenerator import *
from Generators.TektronixGenerator import *
# Very global dictionary for all devices?
# prettier graphs:
pG.setConfigOptions(antialias=True)
# very global variables:
ON = "ON"
OFF = "OFF"

class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super(MainWindow, self).__init__()
                self.ui = Ui_MainGuiWindow()
                self.ui.setupUi(self)
                #Normally this is all to be done in order to show a window
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
                self.setupPlotWidget()
                # Other signals:
                self.ui.connectToOscilograph_button.clicked.connect(self.connectOscilograph)
                self.ui.getVoltsFromCH1_button.clicked.connect(self.getVoltsFromCH1_button_clicked)
                self.ui.getVoltasFromCH2_button.clicked.connect(self.getVoltsFromCH2_button_clicked)
                self.ui.getDatafromBothChannels_button.clicked.connect(self.getDatafromBothChannels_button_clicked)
                self.dataCurveOne = self.ui.dataViewWidget.plot()
                self.dataCurveTwo = self.ui.dataViewWidget.plot()
                self.SetupWindow()
                self.ui.useRegularUpdateBox.stateChanged.connect(self.StateChanged)
                # everything related to control of generator:
                self.ui.setSignalAmplitudeButton.clicked.connect(self.setGeneratorsAmplitude)
                self.ui.sendCustomCmd_gen_button.clicked.connect(self.sendCustomGenCmd)
                self.ui.setOffsetButton.clicked.connect(self.setOffset_generator)
                self.ui.setPeriodButton.clicked.connect(self.setPeriod_generator)
                pass

        def setPeriod_generator(self):
                self.checkStateOfRadioButtons()
                period = self.ui.periodBox.value()
                self.Generator.SetPeriod(self.Generator.CH1, period, self.PeriodUnit, self.PeriodPower)
                period = self.Generator.GetPeriod(self.Generator.CH1)
                self.DebugLog("Periodas "+str(period))
                pass

        def setOffset_generator(self):
                offset = self.ui.voltageOffsetBox.value()
                self.Generator.SetOffset(self.Generator.CH1, offset)
                pass

        def sendCustomGenCmd(self):
                cmd = self.ui.cmd_custom_for_generator.currentText()
                self.DebugMessage(cmd, 3000)
                if("?" in cmd):
                        ats = self.Generator.Ask(cmd)
                        self.DebugLog(ats)
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
                self.DebugMessage("State changed, got parameter "+str(int), 1000)
                if (int == 0):
                        # Unchecked
                        pass
                elif (int == 2):
                        # checked state
                        pass
                else:
                        self.DebugMessage("Shit happened "+str(int), 1000)
                        pass
                # self.DebugMessage("")

        def SetupWindow(self):
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("Icons/comport.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setWindowIcon(icon)
                self.dataCurveOne.setPen((200, 200, 100))
                self.dataCurveTwo.setPen((100, 200, 255))
                pass

        def getDatafromBothChannels_button_clicked(self):
                self.getVoltsFromChannel("CHAN1", self.dataCurveOne)
                self.getVoltsFromChannel("CHAN2", self.dataCurveTwo)
                pass

        def getVoltsFromCH2_button_clicked(self):
                self.getVoltsFromChannel("CHAN2", self.dataCurveTwo)
                pass

        def getVoltsFromChannel(self, CH:str, dataCurve):
                data_from_channel, time_array, time_unit = self.Osciloscope.get_data_points_from_channel(CH)
                self.ui.dataViewWidget.setLabel('bottom', 'Time', units=time_unit)
                self.ui.dataViewWidget.setLabel('left', 'Voltage', units='V')
                dataCurve.setData(time_array, data_from_channel)
                self.DebugMessage("Working on it ...", 1000)
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
        def setupPlotWidget(self):
                '''
                Draw correct axes and so on:
                
                :return:
                '''
                self.ui.dataViewWidget.plotItem.showGrid(True, True, 1.0)
                
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
                self.ui.tableWithTCPIPDevices.setColumnCount(4)
                self.ui.tableWithTCPIPDevices.setHorizontalHeaderLabels(["TCP/IP adresas","Gen/Osc?", "Naudoti?", "*IDN?"])
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
                        self.ui.tableWithTCPIPDevices.selectRow(i)
                else:
                        self.ui.tableWithTCPIPDevices.setRowCount(1)
                        self.ui.tableWithTCPIPDevices.setCellWidget(1, 1, QtWidgets.QComboBox())
                        self.ui.tableWithTCPIPDevices.cellWidget(1, 1).addItems(listOfDevices)
                        self.ui.tableWithTCPIPDevices.setCellWidget(1, 2, QtWidgets.QCheckBox())
                        self.ui.tableWithTCPIPDevices.cellWidget(1, 2).setChecked(False)
                        self.ui.tableWithTCPIPDevices.selectRow(1)
                pass
                
        def closeFn(self):
                if self.Generator is not None:
                        # self.Generator.ask("*RST")
                        # Nereikia čia reset'o daryti.
                        self.Generator.Close()
                if self.Osciloscope is not None:
                        self.Osciloscope.close()
                print("Debug: exit")
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
        
        def DebugMessage(self, msg, time=500):
                self.ui.statusbar.showMessage(msg, time)
        
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