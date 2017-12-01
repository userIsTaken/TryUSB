#!/usr/bin/python3
from PyQt5 import QtCore, QtWidgets, QtGui
from UIfiles.GUIThread import Ui_MainGuiWindow

import sys, os
from USBTMC_Devices import *
from GetInfoAboutDevices import *
from ConfigParser import *
import vxi11
import pyqtgraph as pG
# Very global dictionary for all devices?
# prettier graphs:
pG.setConfigOptions(antialias=True)

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
                pass

        def SetupWindow(self):
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("Icons/comport.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setWindowIcon(icon)
                self.dataCurveOne.setPen((200, 200, 100))
                self.dataCurveTwo.setPen((100, 200, 255))

                pass

        def getDatafromBothChannels_button_clicked(self):
                data_from_channel, time_array, time_unit = self.Osciloscope.get_data_points_from_channel("CHAN1")
                self.ui.dataViewWidget.setLabel('bottom', 'Time', units=time_unit)
                self.ui.dataViewWidget.setLabel('left', 'Voltage', units='V')
                # plot = self.ui.dataViewWidget.plot()
                # plot.setPen(200, 200, 100)
                self.dataCurveOne.setData(time_array, data_from_channel)
                self.DebugMessage("Working on it ...", 1000)
                pass
                data_from_channel, time_array, time_unit = self.Osciloscope.get_data_points_from_channel("CHAN2")
                self.ui.dataViewWidget.setLabel('bottom', 'Time', units=time_unit)
                self.ui.dataViewWidget.setLabel('left', 'Voltage', units='V')
                # plot = self.ui.dataViewWidget.plot()
                # plot.setPen(200, 200, 100)
                self.dataCurveTwo.setData(time_array, data_from_channel)
                self.DebugMessage("Working on it ...", 1000)
                pass

        def getVoltsFromCH2_button_clicked(self):
                data_from_channel, time_array, time_unit = self.Osciloscope.get_data_points_from_channel("CHAN2")
                self.ui.dataViewWidget.setLabel('bottom', 'Time', units=time_unit)
                self.ui.dataViewWidget.setLabel('left', 'Voltage', units='V')
                # plot = self.ui.dataViewWidget.plot()
                # plot.setPen(200, 200, 100)
                self.dataCurveTwo.setData(time_array, data_from_channel)
                self.DebugMessage("Working on it ...", 1000)
                pass
        
        def connectOscilograph(self):
                connected_devices = getDevicesFromComboBoxes(self.ui.comboBox_for_generator, self.ui.comboBox_for_oscillograph, self.Devices_dict)
                self.Osciloscope = RigolDS1000SeriesScope(connected_devices[3])
                msg = self.Osciloscope.get_name()
                self.ui.idn_label_oscilograph.setText(msg.decode())
                self.DebugMessage("IDN: "+msg.decode(), 1000)
                self.Osciloscope.set_y_scale("CHAN1", "2")
                self.Osciloscope.set_time_scale("0.000002")
                pass

        def getVoltsFromCH1_button_clicked(self):

                data_from_channel, time_array, time_unit = self.Osciloscope.get_data_points_from_channel("CHAN1")
                self.ui.dataViewWidget.setLabel('bottom', 'Time', units=time_unit)
                self.ui.dataViewWidget.setLabel('left', 'Voltage', units='V')
                # plot = self.ui.dataViewWidget.plot()
                # plot.setPen(200, 200, 100)
                self.dataCurveOne.setData(time_array, data_from_channel)
                self.DebugMessage("Working on it ...", 1000)
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
                        self.Generator.ask("C1:OUTP ON")
                        self.DebugMessage("CH1 ON", 1000)
                else:
                        self.Generator.ask("C1:OUTP OFF")
                        self.DebugMessage("CH1 OFF", 1000)
                pass
        
        def changeOutputCH2(self):
                if (self.ui.InputOutputCH2Button.isChecked()):
                        self.Generator.ask("C2:OUTP ON")
                        self.DebugMessage("CH2 ON", 1000)
                else:
                        self.Generator.ask("C2:OUTP OFF")
                        self.DebugMessage("CH2 OFF", 1000)
                pass
        
        def runInitGenerator(self):
                listOfCommands = getTextLinesFromQTextEditField(self.ui.initialConfigurationForGenerator)
                # print("List contains:")
                # for i in listOfCommands:
                #         print(i)
                for i in listOfCommands:
                        message = self.Generator.ask(str(i))
                        self.DebugLog(message)
                        self.ui.statusbar.showMessage(message, 500)
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
                self.Generator = vxi11.Instrument(Gen)
                self.DebugLog("Testas prisijungimo")
                self.ui.connection_status_label.setText(self.Generator.ask("*IDN?"))
                #  populate init commands from file:
                myConf = Configuration("Configs/Siglent.ini")
                lines = myConf.readDefaultInitCommandsForSiglent("SIGLENT INIT CONFIG", "InitCMD")
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
                        self.Generator.ask("*RST")
                        self.Generator.close()
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
                                        dvs.reset()
                                        dvs.close()
                                except Exception as e:
                                        print("Scan function failed")
                                        print(e.args)
                                        print(e)
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