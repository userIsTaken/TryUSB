import os, sys
import configparser

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

        def USBTMCDevicesSaver(self):
                pass

        def USBTMCDevicesLoader(self):
                pass