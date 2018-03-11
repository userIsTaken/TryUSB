import os, sys
import vxi11
from ConfigParser import *


class SiglentGenerator_TCP():
        '''
        Class for TCP-enabled Siglent generators
        Note that SCPI command strings must be terminated with a “\n” (new line)
character in programming. {From official programming guide}
        '''
        
        def __init__(self, gen_path: str):
                '''

                :param gen_path: path (IP) for generator
                '''
                self.Instrument = vxi11.Instrument(gen_path)
                self.CH1 = "C1"
                self.CH2 = "C2"
                self.IDN = None
                # channel 1 - CH1, channel 2 - CH2
                pass
        
        def GetIDN(self):
                name = self.Instrument.ask("*IDN?")
                return name
        
        def EnableOutput(self, channel, out: str):
                self.Instrument.ask(channel+":OUTP "+out)
        
        def GetInitConfiguration(self):
                myConf = Configuration("Configs/Siglent.ini")
                lines = myConf.readDefaultInitCommands("SIGLENT INIT CONFIG", "InitCMD")
                return lines
                pass
        
        def Ask(self, cmd:str):
                self.Instrument.ask(cmd)
                pass
        
        def Write(self, cmd):
                self.Instrument.write(cmd)
                pass
        
        def Close(self):
                self.Instrument.close()
                pass

        def GetAmplitude(self, channel):
                '''
                In Volts,

                :param channel: string of channel
                :return: ampl in Volts
                '''
                command = channel+":BSWV AMP?"
                amplitude = self.Ask(command)
                return amplitude
                pass

        def SetNormalizedOffSet(self):
                pass

        def GetNormalizedOffset(self):
                pass

        def SetOffset(self, channel, offset):
                '''

                :param channel:
                :param offset:
                :return:
                '''
                command = channel+":BSWV OFST "+offset
                self.Instrument.write(command)
                pass

        def GetOffset(self, channel):
                command = channel + ":BSWV OFST?"
                offset = self.Instrument.ask(command)
                return offset
                pass

        def SetPeriod(self, channel, period):
                command = channel+":BSWV PERI "+period
                self.Instrument.write(command)
                pass

        def GetPeriod(self, channel):
                command = channel + ":BSWV PERI?"
                period = self.Instrument.ask(command)
                return period
                pass

        def SetFrequency(self, channel, freq):
                command = channel+":BSWV FRQ "+freq
                self.Instrument.write(command)
                pass

        def GetFrequency(self, channel):
                command = channel + ":BSWV FRQ?"
                frequency = self.Instrument.ask(command)
                return frequency
                pass

        def SetTriggerSource(self, source):
                '''

                :param source: EXT, INT, MAN
                :return:
                '''
                command= ":IQ:TRIG:SOUR "+source
                self.Instrument.write(command)
                pass