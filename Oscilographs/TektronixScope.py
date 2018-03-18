import os, sys, time
import vxi11
from ConfigParser import *
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
from Units.UnitCheck import *
import traceback
from ConfigParser import *


class TektronixScope_TCP(QObject):
        '''
        
        '''
        cmd_emiter = pyqtSignal(str)
        
        def __init__(self, path: str):
                '''
                
                :param gen_path: path (IP) for generator
                '''
                super(TektronixScope_TCP, self).__init__()
                self.Instrument = vxi11.Instrument(path)
                # self.Instrument.timeout = 1
                self.CH1 = "CH1"
                self.CH2 = "CH2"
                self.CH3 = "CH3"
                self.CH4 = "CH4"
                self._channels = {"1": self.CH1, "2": self.CH2, "3": self.CH3, "4": self.CH4}
                self.signalChannel = None
                self.responseChannel = None
                self.IDN = self.Instrument.ask("*IDN?")
                # channel 1 - CH1, channel 2 - CH2
                pass
        
        def get_init_conf(self):
                # try:
                myConf = Configuration("Configs/TextronixScope.ini")
                lines = myConf.readDefaultInitCommands("TEKTRONIX OSC INIT CONFIG", "InitTektronixOsc")
                return lines
                # except Exception as ex:
                #         print(str(ex))
                #         pass
                pass
        
        def write(self, command):
                """Send an arbitrary command directly to the scope"""
                self.cmd_emiter.emit(str(command))
                self.Instrument.write(command)
                pass
        
        def get_name(self):
                '''
                
                :return:
                '''
                name = self.Instrument.ask("*IDN?")
                return name
                pass
        
        def read(self, command):
                """Read an arbitrary amount of data directly from the scope"""
                self.cmd_emiter.emit(str(command))
                answer = self.Instrument.ask(command)
                return answer
                pass
        
        def reset(self):
                self.Instrument.write("*RST")
        
        def close(self):
                self.Instrument.close()
        
        def stop(self):
                self.Instrument.write("ACQUIRE:STATE STOP")
                pass
        
        def set_channels_mode(self, mode):
                '''
                Tektronix does not support this command, just pass over it.

                :param mode:
                :return:
                '''
                pass
        
        def get_channels_mode(self):
                '''
                Tektronix does not support this command

                :return: always return NORM
                '''
                return "NORM"
                pass
        
        def get_data_from_channel(self, channel, length=9000):
                pass
        
        def get_channel_scale(self, CH: str):
                '''
                Vertical scale of channel
                
                :param CH: (str) channel CH1, CH2, CH3, CH4 ...
                :return:
                '''
                scale = self.Instrument.ask(CH + ":SCA?")
                return scale
                pass
        
        def get_channel_CHAN2_scale(self):
                pass
        
        def get_time_scale(self):
                # HORIZONTAL: SCALE?
                h_scale = float(self.Instrument.ask("HORIZONTAL:SCALE?"))
                # nmb, preffix = getNumberSIprefix(h_scale)
                return h_scale
                pass
        
        def get_time_offset(self):
                pass
        
        def get_time_array(self, dataCHANNEL):
                pass
        
        def get_channel_offset(self, CHANNEL):
                '''
                
                :param CHANNEL:
                :return:
                '''
                
                cmd = CHANNEL + ":OFF?"
                channel_offset = self.Instrument.ask(cmd)
                return channel_offset
                pass
        
        def set_channel_offset(self, CHANNEL, OFFset: str):
                '''
                
                :param CHANNEL:
                :param OFFset:
                :return:
                '''
                
                cmd = CHANNEL + ":OFFS " + OFFset
                self.Instrument.write(cmd)
                
                pass
        
        def set_channel_position(self, CHANNEL, POSset: str, OFST=0):
                cmd = CHANNEL + ":POS " + "-3"
                set_offset = OFST
                self.Instrument.write(cmd)
                self.set_channel_offset(CHANNEL, str(set_offset))
                pass
        
        def get_channel_position(self, CHANNEL):
                cmd = CHANNEL + ":POS?"
                position = self.Instrument.ask(cmd)
                return position
        
        def get_data_points_from_channel(self, CH: str):
                '''
                Use this function in order to get all data points from scope:
                
                :param CH: specify a channel, str
                :return: array of time and data points, time unit
                '''
                # % retrieve
                # vertical
                # scaling
                # informaiton
                # yof = query(dpo, ':wfmo:yof?;', '%s', '%E');
                # ymu = query(dpo, ':wfmo:ymu?;', '%s', '%E');
                # yze = query(dpo, ':wfmo:yze?;', '%s', '%E');

                try:
                        self.Instrument.write("DATA:SOURCE " + CH)

                        # ASCII encoding:
                        # WFMOutpre: ENCdg
                        # {ASCii | BINary}

                        self.Instrument.write("WFMO:ENC ASCii")

                        yof = float(self.Instrument.ask("WFMO:YOF?"))
                        ymu = float(self.Instrument.ask("WFMO:YMU?"))
                        yze = float(self.Instrument.ask("WFMO:YZE?"))

                        # % retrieve
                        # horizontal
                        # scaling
                        # information
                        # nrp = query(dpo, ':wfmo:nr_p?;', '%s', '%E');
                        # xin = query(dpo, ':wfmo:xin?;', '%s', '%E');
                        # xze = query(dpo, ':wfmo:xze?;', '%s', '%E');

                        nrp = float(self.Instrument.ask("WFMO:NR_P?"))
                        xin = float(self.Instrument.ask("WFMO:XIN?"))
                        xze = float(self.Instrument.ask("WFMO:XZE?"))

                        # get all the data:
                        Y_array = self.Instrument.ask("CURVE?")
                        Y = Y_array.split(",")
                        # (double('wave')-yof).*ymu+yze
                        dataCH2 = [(float(x) - yof) * ymu + yze for x in Y]
                        # time array: scaled_time = linspace(xze,xze+(xin*nrp),nrp);
                        time_array = np.linspace(xze, xze + (xin * nrp), nrp)
                        scale = self.get_time_scale()
                        print("Scale : ", scale)
                        value, time_unit = getNumberSIprefix(scale)
                        # print("time value and time unit:", value, time_unit)
                        # time_unit = "OMS!"
                        # print("length of Y", len(Y))
                        # print("length of time", len(time_array))
                        return np.asarray(dataCH2), time_array, "S"  # hardcoded time unit for Tektronix
                except Exception as ex:
                        return 9999, 9999, "S"
                        pass
                # return np.asarray(dataCH2), time_array, "S"  # hardcoded time unit for Tektronix
                pass
        
        def run(self):
                self.Instrument.write("ACQUIRE:STATE RUN")
                pass
        
        def unlock_key(self):
                '''
                
                :return:
                '''
                cmd = "UNL ALL"  # unlock all knobs and buttons
                self.Instrument.write(cmd)
                
                pass
        
        def set_y_scale(self, CHAN, y_scale: str, sleep_time=0.5, yUnit="V"):
                '''
                Sets Y scale for a specified channel:
                
                :param yUnit:
                :param CHAN: channel
                :param y_scale: volts
                :param sleep_time: not used, 0.5 s default
                :return:
                '''
                
                cmd_unit = CHAN + ":YUN " + "\"" + yUnit + "\""
                self.Instrument.write(cmd_unit)
                # we can pass any value, default it will be in Volts
                cmd = CHAN + ":SCA " + y_scale  # Volts?
                self.Instrument.write(cmd)
                pass

        def set_closest_voltage_scale(self, chan, scale):
                scale_str = "1"
                if 10 > scale >= 2:
                        scale_str = str("{0:.1f}".format(scale))
                        print(chan + " signalo skalė: " + str(scale_str))
                elif 1 > scale >= 0.1:
                        scale_str = str("{0:.2f}".format(scale))
                        print(chan + "signalo skalė: " + str(scale_str))
                elif 0.1 > scale >= 0.02:
                        scale_str = str("{0:.3f}".format(scale))
                        print(chan + "signalo skalė: " + str(scale_str))
                elif 0.02 > scale >= 0.002:
                        scale_str = str("{0:.4f}".format(scale))
                        print(chan + "signalo skalė: " + str(scale_str))
        
                self.set_y_scale(chan, scale_str)
                pass
        
        def set_time_scale(self, time_scale: str):
                cmd = "HOR:SCA " + str(time_scale)
                print("DEBUG: TEKTRONIX TIME SCALE ", cmd)
                self.Instrument.write(cmd)
                pass
        
        def set_closest_time_scale(self, time_scale, time_unit):
                '''
                
                :param time_scale:
                :param time_unit:
                :return:
                '''
                
                print("TEKTRONIX OSC||DEBUG: t scale, t unit", time_scale, time_unit)
                
                array = [400, 200, 100, 40, 20, 10, 4, 2, 1]  # can not be ns?
                time_value = None
                time_power = None
                for i in array:
                        if (math.isclose(time_scale, i, rel_tol=0.45)):
                                time_value = i
                                print("DEBUG: SELCTED TEKTRONIX TIME VALUE ", str(time_value))
                                break
                                pass
                        pass
                if ("uS" == time_unit) or ("µS" == time_unit):
                        time_power = 10 ** (-6)
                        req_time_scale = time_value * time_power
                        self.set_time_scale(str("{0:.8f}".format(req_time_scale)))
                        pass
                elif "mS" == time_unit:
                        time_power = 1e-3
                        req_time_scale = time_value * time_power
                        self.set_time_scale(str("{0:.8f}".format(req_time_scale)))
                        pass
                elif "S" == time_unit:
                        time_power = 1e0
                        req_time_scale = time_value * time_power
                        self.set_time_scale(str("{0:.8f}".format(req_time_scale)))
                        pass
                else:
                        print("We can not be here - check a code!")
                        pass
                
                pass
                
                # self.set_time_scale(time_scale)
                pass
        
        def set_time_offset(self, time_offset: str, sleep_time=0.5):
                cmd = "HOR:POS " + "90"
                self.Instrument.write(cmd)
                pass
        
        def set_trigger_mode(self, mode):
                '''
                It uses A trigger!
                
                :param mode: EDGE, etc ...
                :return:
                '''
                cmd = "TRIG:A:TYP " + mode
                self.Instrument.write(cmd)
                pass
        
        def get_trigger_mode(self):
                '''
                It uses A trigger
                
                :return: mode of trigger (EDGE, etc ...)
                '''
                cmd = "TRIG:A:TYP?"
                mode = self.Instrument.ask(cmd)
                return mode
        
        def set_trigger_source(self, source):
                '''
                
                :param source: CH1, CH2, etc ...
                :return:
                '''
                cmd = "TRIG:A:EDGE:SOU " + source
                self.Instrument.write(cmd)
                pass
        
        def set_trigger_edge_level(self, level: str):
                cmd = "TRIG:A:LEV " + level
                self.Instrument.write(cmd)
                pass
        
        def set_channel_input_terminator(self, CH, terminator='M'):
                if terminator == 'M' or terminator == 1e6 or terminator == "m":
                        cmd = CH + ":TER " + "MEG"
                        self.Instrument.write(cmd)
                elif terminator == "F" or terminator == 50 or terminator == 'f':
                        cmd = CH + ":TER " + "FIF"
                        self.Instrument.write(cmd)
                        pass
                else:
                        print("Wrong argument")
                pass
        
        def get_channel_input_terminator(self, CH):
                terminator = self.Instrument.ask(CH + ":TER?")
                return terminator
