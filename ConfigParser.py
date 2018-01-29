import os, sys
import configparser
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

        def ConfigFileLoader(self, tableWidget):
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
                        for dkey in dev_dic:
                                print(dkey, dev_dic[dkey])
                                pass
                        # ADD row, insert values:
                        
                        pass
                pass
        
        def getKeyValue(self, string):
                par_string = string.split("\n")
                dev_dic = {}
                for i in par_string:
                        entry, value = i.split(":")
                        print(entry, value, "ev")
                        dev_dic[entry]=value
                return dev_dic
                pass

        def ConfigFileSaver(self, tableWidget):
                pass

        def USBTMCDevicesSaver(self, gui:Ui_MainGuiWindow):
                """

                :param gui:
                :return:
                """
                pass

        def USBTMCDevicesLoader(self, gui:Ui_MainGuiWindow):
                path = None
                idn = None
                dev_dict = {}
                self.config.read(self.FilePath)
                section = "USBTMC devices"
                for key in self.config[section]:
                        if key == "generator":
                                print("gen")
                                value = self.config[section][key]
                                if len(value) == 0:
                                        print(value)
                                        pass
                                else:
                                        idn, path = value.split("|")
                                        dev_dict["gen"] = (path, idn)
                                        gui.comboBox_for_generator.addItem(idn)
                                        #
                                        pass
                                pass
                        elif key == "oscilograph":
                                print("osc")
                                value = self.config[section][key]
                                if len(value) == 0:
                                        print(value)
                                        pass
                                else:
                                        idn, path = value.split("|")
                                        dev_dict["osc"] = (path, idn)
                                        gui.comboBox_for_oscillograph.addItem(str(idn))
                                        pass
                                pass
                        else:
                                print("Some stupid situation in ConfigParser.py")
                return dev_dict
                pass