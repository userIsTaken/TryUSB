import  os, sys, time
import vxi11
from ConfigParser import *

class TektronixScope_TCP():
        '''
        
        '''
        def __init__(self, path:str):
                '''
                
                :param gen_path: path (IP) for generator
                '''
                self.Instrument = vxi11.Instrument(path)
                # self.Instrument.timeout = 1
                self.CH1 = "SOUR1"
                self.CH2 = "SOUR2"
                self.IDN = None
                # channel 1 - CH1, channel 2 - CH2
                pass
        
        def get_name(self):
                '''
                
                :return:
                '''
                name = self.Instrument.ask("*IDN?")
                return name
                pass