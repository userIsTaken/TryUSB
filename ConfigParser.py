import os, sys
import configparser
from PyQt5 import QtCore, QtWidgets, QtGui
from UIfiles.GUIThread import Ui_MainGuiWindow

class Configuration:
        def __init__(self, FilePath):
                self.FilePath = FilePath
                self.config = configparser.ConfigParser()
                pass

        
        def readDefaultInitCommands(self, section, option : str):
                self.config.read(self.FilePath)
                longString=self.config.get(section, option)
                return longString
                pass

        def ConfigTCPIPLoader(self, tableWidget):
                '''
                Load IP devices
                
                :param tableWidget:
                :return:
                '''
                
                self.config.read(self.FilePath)
                section = "TCP IP devices"
                for key in self.config[section]:
                        print(key)
                        print(self.config[section][key])
                        # TODO add parsing:
                        dev_dic = self.getKeyValue(self.config[section][key])
                        # for dkey in dev_dic:
                        #         # print(dkey, dev_dic[dkey])
                        #         pass
                        # ADD row, insert values:
                        self.addRow(tableWidget, dev_dic)
                        pass
                pass
        
        def addRow(self, tWidget, dev_dict):
                listOfDevices = ["Generatorius", "Oscilografas"]
                IP = dev_dict["IP"]
                GENOSCI = dev_dict["GENOSCI"]
                USE = dev_dict["USE"]
                IDN = dev_dict["IDN"]
                i = tWidget.rowCount()
                if i is not None:
                        tWidget.setRowCount(i + 1)
                        cell = QtWidgets.QTableWidgetItem()
                        cell.setText(str(IP))
                        tWidget.setItem(i, 0, cell)
                        tWidget.setCellWidget(i, 1, QtWidgets.QComboBox())
                        tWidget.cellWidget(i, 1).addItems(listOfDevices)
                        if "gen" in GENOSCI.lower():
                                tWidget.cellWidget(i,1).setCurrentIndex(0)
                                pass
                        elif "osc" in GENOSCI.lower():
                                tWidget.cellWidget(i, 1).setCurrentIndex(1)
                                pass
                        else:
                                pass
                        tWidget.setCellWidget(i, 2, QtWidgets.QCheckBox())
                        if "yes" in USE.lower():
                                tWidget.cellWidget(i, 2).setChecked(True)
                                pass
                        else:
                                tWidget.cellWidget(i, 2).setChecked(False)
                                pass
                        # tWidget.cellWidget(i, 2).setChecked(False)
                        cell = QtWidgets.QTableWidgetItem()
                        cell.setText(str(i))
                        tWidget.setItem(i, 4, cell)
                        tWidget.selectRow(i)
                else:
                        tWidget.setRowCount(1)
                        cell = QtWidgets.QTableWidgetItem()
                        cell.setText(str(IP))
                        tWidget.setItem(1, 0, cell)
                        tWidget.setCellWidget(1, 1, QtWidgets.QComboBox())
                        tWidget.cellWidget(1, 1).addItems(listOfDevices)
                        if "gen" in GENOSCI.lower():
                                tWidget.cellWidget(1,1).setCurrentIndex(0)
                                pass
                        elif "osc" in GENOSCI.lower():
                                tWidget.cellWidget(1, 1).setCurrentIndex(1)
                                pass
                        else:
                                pass
                        tWidget.setCellWidget(1, 2, QtWidgets.QCheckBox())
                        if "yes" in USE.lower():
                                tWidget.cellWidget(1, 2).setChecked(True)
                                pass
                        else:
                                tWidget.cellWidget(1, 2).setChecked(False)
                                pass
                        
                        cell = QtWidgets.QTableWidgetItem()
                        cell.setText(str(1))
                        tWidget.setItem(1, 4, cell)
                        # tWidget.selectRow(1)
                pass
        
        def getKeyValue(self, string):
                par_string = string.split("\n")
                dev_dic = {}
                for i in par_string:
                        entry, value = i.split(":")
                        # print(entry, value, "ev")
                        dev_dic[entry]=value
                return dev_dic
                pass


        def DevicesSaver(self,file:str, gui:Ui_MainGuiWindow):
                """

                :param gui:
                :return:
                """
                tableWidget = gui.tableWithTCPIPDevices
                comboGen = gui.comboBox_for_generator
                comboOsc = gui.comboBox_for_oscillograph
                #
                
                
                
                pass

        def USBTMCDevicesLoader(self):
                '''
                
                :return:
                '''
                dev_dict= {}
                self.config.read(self.FilePath)
                section = "USBTMC devices"
                for key in self.config[section]:
                        dev_dict[key]=self.config[section][key]
                        # print(self.config[section][key])
                        pass
                return dev_dict