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
                # self.Instrument.timeout = 1
                self.CH1 = "SOUR1"
                self.CH2 = "SOUR2"
                self.IDN = None
                # channel 1 - CH1, channel 2 - CH2
                pass

        def GetIDN(self):
                name = self.Instrument.ask("*IDN?")
                return name

        def EnableOutput(self, channel, out: str):
                '''
                
                :param channel: self.object.ch1 or ch2
                :param out: str ON, OFF
                :return:
                '''
                if "1" in channel:
                        self.Instrument.write("OUTP1:STAT "+out)
                        # self.Instrument.
                        # pass
                elif "2" in channel:
                        self.Instrument.write("OUTP2:STAT " + out)
                        pass
                else:
                        print("Stupid argument")
                        pass
                pass

        def GetInitConfiguration(self):
                myConf = Configuration("Configs/Tektronix.ini")
                lines = myConf.readDefaultInitCommands("TEKTRONIX INIT CONFIG", "InitCMD")
                return lines
                pass

        def Ask(self, cmd: str):
                return self.Instrument.ask(cmd)
                pass

        def Close(self):
                self.Instrument.close()
                pass
        
        def Write(self, cmd:str):
                self.Instrument.write(cmd)
                pass
        
        def SetAmplitude(self, channel, amplitude):
                # cmd = "SOUR1:VOLT:LEV:IMM:AMP 1VPP"
                cmd = channel+":VOLT:LEV:IMM:AMPL "+str(amplitude)+"VPP"
                self.Write(cmd)
                pass
        
        def GetAmplitude(self, channel):
                pass
        
        def SetOffset(self, channel, offset):
                pass
        
        def GetOffset(self, channel):
                pass
        
        def SetPeriod(self, channel, period, power, unit):
                '''

                Tektronix seems able to set just a frequency. Workaround is setting a frequency,
                calculated from period, using well known relation:
                ν = 1 / T

                :param channel: CH1 or CH2
                :param period: period
                :param power: power of period
                :param unit: μs, ms or s
                :return:
                '''

                freq = 1 / period
                freq_pow = None
                if("uS" in unit):
                        freq_pow = "MHz"
                        pass
                elif("mS" in unit):
                        freq_pow = "kHz"
                        pass
                elif("S" == unit):
                        freq_pow = "Hz"
                        pass
                else:
                        pass
                pass
        
        def GetPeriod(self, channel):
                pass
        
        def SetFrequency(self, channel, freq):
                pass
        
        def GetFrequency(self, channel):
                pass