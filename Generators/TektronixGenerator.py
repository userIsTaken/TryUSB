import  os, sys
import vxi11


class TektronixGenerator_TCP():
        '''
        Class for TCP-enabled Tektronix generators
        '''
        def __init__(self, gen_path:str):
                '''
                
                :param gen_path: path (IP) for generator
                '''
                self.Instrument = vxi11.Instrument(gen_path)
                self.CH1 = "SOUR1"
                self.CH2 = "SOUR2"
                pass
        
        def GetIDN(self):
                name = self.Instrument.ask("*IDN?")
                return name
        
        