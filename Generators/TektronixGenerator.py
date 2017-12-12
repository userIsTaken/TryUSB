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
        
        def SetPeriod(self, channel, period, unit, power):
                '''

                Tektronix seems able to set just a frequency. Workaround is setting a frequency,
                calculated from period, using well known relation:
                ν = 1 / T
                cmd:SOUR1:FREQ:FIX 100kHz

                :param channel: CH1 or CH2
                :param period: period
                :param power: power of period
                :param unit: μs, ms or s
                :return:
                '''

                freq = 1 / period
                freq_pow = None
                if("uS" == unit):
                        freq_pow = "MHz"
                        # print(freq_pow +" " + unit)
                        pass
                elif("mS" == unit):
                        freq_pow = "kHz"
                        # print(freq_pow + " " + unit)
                        pass
                elif("S" == unit):
                        freq_pow = "Hz"
                        # print(freq_pow + " " + unit)
                        pass
                else:
                        pass
                cmd_freq = channel+":FREQ:FIX "+str(freq)+freq_pow
                # pass it into other function:

                self.Write(cmd_freq)
                pass
        
        
        def GetPeriod(self, channel):
                '''
                Need workaround - there aren't any functions related to the period
                
                :param channel:
                :return:
                '''
                sfreq = self.GetFrequency(channel)
                freq = float(sfreq)
                period = 1/freq
                return period
        
        def SetFrequency(self, channel:str, freq:float, freq_pow="kHz"):
                '''
                Sets a channels frequency.
                
                :param channel:
                :param freq: integer
                :param freq_pow: Hz|kHz|MHz, default : kHz
                :return:
                '''
                cmd_freq = channel + ":FREQ:FIX " + str(freq) + freq_pow
                self.Write(cmd_freq)
                pass
        
        def GetFrequency(self, channel):
                '''
                Gets frequency from channel
                
                :param channel:
                :return:
                '''
                ask_freq = channel+":FREQ:FIX?"
                ask_freq = self.Ask(ask_freq)
                return  ask_freq
                pass