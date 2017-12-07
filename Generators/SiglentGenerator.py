import os, sys
import vxi11


class SiglentGenerator_TCP():
        '''
        Class for TCP-enabled Siglent generators
        '''
        
        def __init__(self, gen_path: str):
                '''

                :param gen_path: path (IP) for generator
                '''
                self.Instrument = vxi11.Instrument(gen_path)
                self.CH1 = "C1"
                self.CH2 = "C2"
                # channel 1 - CH1, channel 2 - CH2
                pass
        
        def GetIDN(self):
                name = self.Instrument.ask("*IDN?")
                return name
        
        def EnableOutput(self, channel:str, out:bool):
                pass