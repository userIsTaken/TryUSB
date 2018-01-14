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

                                        gui.comboBox_for_oscillograph.addItem(str(value))
                                        pass
                                pass
                        else:
                                pass

                pass