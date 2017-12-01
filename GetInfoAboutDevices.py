import os, sys
from PyQt5 import QtCore, QtWidgets, QtGui
from USBTMC_Devices import *

def getDevicesFromComboBoxes(comboGenerator, comboOsciloscope : QtWidgets.QComboBox, Devices_dic):
        Osciloscope=None
        Generator=None
        PathOsciloscope=None
        PathGenerator=None
        activeGenerator = comboGenerator.currentText() # there is an IDN
        activeOsciloscope = comboOsciloscope.currentText()
        if activeGenerator != "[Nėra]":
                Generator = activeGenerator
                # PathGenerator=Devices_dic[activeGenerator]
                for key,value in Devices_dic.items():
                        if value == activeGenerator:
                                PathGenerator = key
                        pass
                pass
        else:
                pass
        # It returns none, if no device detected
        if activeOsciloscope != "[Nėra]":
                Osciloscope = activeOsciloscope
                # PathOsciloscope=Devices_dic[activeOsciloscope]
                for key,value in Devices_dic.items():
                        if value == activeOsciloscope:
                                PathOsciloscope = key
                        pass
                pass
                
        else:
                pass
        return Generator, PathGenerator, Osciloscope, PathOsciloscope
        # IDN
        pass

def getDevicesFromTable(tableWidget: QtWidgets.QTableWidget):
        Devices_list={}
        DeviceRole=None
        DevicePath=None
        l = tableWidget.rowCount()
        dummy_index=0
        while (dummy_index<l):
                if( tableWidget.cellWidget(dummy_index,2).isChecked()):
                        DevicePath = tableWidget.item(dummy_index,0).text()
                        DeviceRole = tableWidget.cellWidget(dummy_index,1).currentText()
                        Devices_list[DeviceRole]=DevicePath
                        pass
                dummy_index=dummy_index+1
                pass
        return Devices_list
        pass

def getDevicePathWithRoleFromList(Role: str, Devices_list : dict):
        '''
        
        :param Role: string
        :param Devices_list: dictionary
        :return: DevicePath string
        '''
        # iteration:
        DevicePath=None
        if Role in Devices_list:
                DevicePath = Devices_list[Role]
        else:
                pass
        return DevicePath
        pass

def getTextLinesFromQTextEditField(QTextEdit: QtWidgets.QTextEdit):
        '''
        
        :param QTextEdit: textEdit field
        :return: list of lines
        '''
        Lines = [] # empty list
        plainText = QTextEdit.toPlainText()
        Lines = plainText.split("\n")
        return Lines
        pass

def scan_USBTMC_devices(mypath:str, devices_dic:dict):
       pass