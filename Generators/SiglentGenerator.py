import os, sys
import vxi11
from ConfigParser import *
from Units.UnitCheck import *
import time


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
                self.TRIG_INT = "INT"
                self.TRIG_EXT = "EXT"
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
                parameters = self.get_inner_parameters(channel)
                for k in parameters:
                        print("KEY : ", k)
                amplitude = parameters["AMP"]
                return amplitude[:-1]
                pass

        def GetNormalizedOffset(self, channel):
                offset = self.GetOffset(channel)
                ampl = self.GetAmplitude(channel)
                print("Siglent offset and ampl", offset, ampl)
                normalized_offset = float(offset) - float(ampl) / 2
                return normalized_offset
                # pass

        def SetNormalizedOffset(self, channel, offset, amplitude):
                gen_offset = amplitude / 2 + offset
                self.SetOffset(channel, gen_offset)
                pass

        def SetNormalizedAmplOffs(self, channel, ampl, offs):
                gen_offset = ampl / 2 + offs
                self.SetAmplitude(channel, ampl)
                self.SetOffset(channel, gen_offset)
                pass

        def SetOffset(self, channel, offset):
                '''

                :param channel:
                :param offset:
                :return:
                '''
                command = channel+":BSWV OFST,"+offset
                self.Instrument.write(command)
                pass

        def GetOffset(self, channel):
        
                parameters = self.get_inner_parameters(channel)
                offset = parameters["OFST"]
                return offset[:-1]
                pass

        def SetPeriod(self, channel, period):
                command = channel+":BSWV PERI,"+period
                self.Instrument.write(command)
                pass

        def GetPeriod(self, channel):
                command = channel + ":BSWV PERI?"
                period = self.Instrument.ask(command)
                return period
                pass

        def SetFrequency(self, channel, freq):
                command = channel+":BSWV FRQ,"+freq
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

        def SetAmplitude(self, channel, amplitude):
                command = channel+":BSWV AMP,"+str(amplitude)
                self.Instrument.write(command)
                pass
        
        def GetTriggerInterval(self, channel=None):
                if channel is None:
                        cmd =self.CH1+":BTWV PRD?"
                        pass
                else:
                        cmd = channel+":BTWV PRD?"
                
                trigger_interval = self.Instrument.ask(cmd)
                return trigger_interval
                pass
        
        def SetTriggerInterval(self, interval, unit:str, channel=None):
                if channel is None:
                        interv = getNumberFromSIprefix(interval, unit)
                        cmd = self.CH1+":BTWV PRD,"+interv
                        pass
                else:
                        interv = getNumberFromSIprefix(interval, unit)
                        cmd = channel + ":BTWV PRD," + interv
                self.Instrument.write(cmd)
                pass
        
        def get_inner_parameters(self, channel, mode="BSWV"):
                try:
                        params_dict = {}
                        cmd = channel+":"+mode+"?"
                        output = self.Instrument.ask(cmd)
                        print("OUTPUT SIGLENT:", output)
                        out_list = output.split()
                        print(out_list, "OUTPUT LIST SIGLENT")
                        param_list = out_list[1]
                        params = param_list.split(",")
                        print("PARAMS SIGLENT", params)
                        i = 0
                        l = len(params)
                        print(l, "LEN(PARAMS)")
                        while i < l-1:
                                params_dict[params[i]]=params[i+1]
                                i = i + 2
                        return params_dict
                except Exception as ex:
                        print(str(ex), "get_inner_parameters")