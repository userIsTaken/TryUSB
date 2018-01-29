from Oscilographs.USBTMC_Devices import *
from Generators.SiglentGenerator import *
from Generators.TektronixGenerator import *
import vxi11

from UIfiles.GUIThread import Ui_MainGuiWindow

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

def GetGenerator(gui:Ui_MainGuiWindow, usbtmc_dev_dict):
        '''

        :param gui:
        :param usbtmc_dev_dict:
        :return:
        '''
        USBTMCGenerator = gui.comboBox_for_generator.currentText()
        devices_from_IPtable = getDevicesFromTable(gui.tableWithTCPIPDevices)
        Generator = None
        try:
                if "Generatorius" in devices_from_IPtable:
                        if devices_from_IPtable["Generatorius"] is not None:
                                dev = vxi11.Instrument(devices_from_IPtable["Generatorius"])
                                name = dev.ask("*IDN?")
                                dev.close() # init will occur later
                                if "Siglent".lower() in name.lower():
                                        Generator = SiglentGenerator_TCP(devices_from_IPtable["Generatorius"])
                                elif "Tektronix".lower() in name.lower():
                                        Generator = TektronixGenerator_TCP(devices_from_IPtable["Generatorius"])
                                pass
                elif USBTMCGenerator != "[Nėra]":
                        # Generator = RigolDS1000SeriesScope()
                        Generator = None
        except Exception as ex:
                print("Generatoriaus gavimo klaida", str(ex))
                pass

        return Generator
        pass

def GetOscilograph(gui:Ui_MainGuiWindow, usbtmc_dev_dict):
        '''

        :param gui:
        :param usbtmc_dev_dict:
        :return:
        '''
        USBTMOscilograph = gui.comboBox_for_oscillograph.currentText()
        devices_from_IPtable = getDevicesFromTable(gui.tableWithTCPIPDevices)
        Oscilograph = None
        dev_path = None
        try:
                if "Oscilografas" in devices_from_IPtable:
                        if devices_from_IPtable["Oscilografas"] is not None:
                                dev = vxi11.Instrument(devices_from_IPtable["Oscilografas"])
                                name = dev.ask("*IDN?")
                                dev.close() # init will occur later
                                if "Tektronix".lower() in name.lower():
                                        pass
                elif USBTMOscilograph != "[Nėra]":
                        for key, value in usbtmc_dev_dict.items():
                                if value == USBTMOscilograph:
                                        dev_path = key
                                pass
                        Oscilograph = RigolDS1000SeriesScope(dev_path)
                        pass
                pass
        except Exception as ex:
                print("Problems with Oscilograph", str(ex))
                pass
        return Oscilograph
        pass