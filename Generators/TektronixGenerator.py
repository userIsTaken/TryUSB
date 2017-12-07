import  os, sys
import vxi11
from ConfigParser import *


class TektronixGenerator_TCP():
        '''
        Class for TCP-enabled Tektronix generators
        '''

        def __init__(self, gen_path: str):
                '''

                :param gen_path: path (IP) for generator
                '''
                self.Instrument = vxi11.Instrument(gen_path)
                self.Instrument.timeout = 100
                self.CH1 = "SOUR1"
                self.CH2 = "SOUR2"
                # channel 1 - CH1, channel 2 - CH2
                pass

        def GetIDN(self):
                name = self.Instrument.ask("*IDN?")
                return name

        def EnableOutput(self, channel, out: str):
                if "1" in channel:
                        self.Instrument.ask("OUTP1:STAT "+out)
                        pass
                elif "2" in channel:
                        self.Instrument.ask("OUTP2:STAT " + out)
                        pass
                else:
                        print("Stupid argument")
                        pass
                pass

        def GetInitConfiguration(self):
                myConf = Configuration("Configs/Siglent.ini")
                lines = myConf.readDefaultInitCommands("SIGLENT INIT CONFIG", "InitCMD")
                return lines
                pass

        def Ask(self, cmd: str):
                self.Instrument.ask(cmd)
                pass

        def Close(self):
                self.Instrument.close()
                pass
        