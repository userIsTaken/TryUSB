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

                pass

        def USBTMCDevicesLoader(self, gui:Ui_MainGuiWindow):
                self.config.read(self.FilePath)
                pass