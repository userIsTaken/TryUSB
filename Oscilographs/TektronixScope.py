import  os, sys, time
import vxi11
from ConfigParser import *
from PyQt5.QtCore import  QObject, pyqtSignal

class TektronixScope_TCP(QObject):
        '''
        
        '''
        cmd_emiter = pyqtSignal(str)
        
        def __init__(self, path:str):
                '''
                
                :param gen_path: path (IP) for generator
                '''
                super(TektronixScope_TCP, self).__init__()
                self.Instrument = vxi11.Instrument(path)
                # self.Instrument.timeout = 1
                self.CH1 = "CH1"
                self.CH2 = "CH2"
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

        def write(self, command):
                """Send an arbitrary command directly to the scope"""
                self.cmd_emiter.emit(str(command))
                self.Instrument.write(command)
                pass

        def read(self, command):
                """Read an arbitrary amount of data directly from the scope"""
                self.cmd_emiter.emit(str(command))
                answer = self.Instrument.ask(command)
                return answer
                pass

        
        def reset(self):
                pass

        def close(self):
                self.Instrument.close()

        def stop(self):
                self.Instrument.write("STOP")
                pass

        def channels_mode(self, mode):
                pass

        def get_channels_mode(self):
                pass

        def get_data_from_channel(self, channel, length=9000):
                pass

        def get_channel_scale(self, CH: str):
                pass

        def get_channel_CHAN2_scale(self):
                pass

        def get_time_scale(self):
                pass
        

        def get_time_offset(self):
                pass

        def get_time_array(self, dataCHANNEL):
                pass

        def get_channel_offset(self, CHANNEL):
                pass

        def set_channel_offset(self, CHANNEL, OFFset: str):
                
                pass

        def get_data_points_from_channel(self, CH: str):
                '''
                Use this function in order to get all data points from scope:
                
                :param CH: specify a channel, str
                :return: array of time and data points, time unit
                '''
                pass

        def run(self):
                
                pass

        def unlock_key(self):
                
                pass

        def set_y_scale(self, CHAN, y_scale: str, sleep_time=0.5):
                
                pass

        def set_time_scale(self, time_scale: str):
                
                pass

        def set_closest_time_scale(self, time_scale, time_unit):
                
                pass

        def set_time_offset(self, time_offset: str, sleep_time=0.5):
                
                pass

        def set_trigger_edge_level(self, level: str):
                
                pass
        
        
        def set_channel_input_terminator(self, CH, terminator='M'):
                if terminator == 'M' or terminator == 1e6 or terminator == "m":
                        cmd = CH+":TER "+"MEG"
                        self.Instrument.write(cmd)
                elif terminator == "F" or terminator == 50 or terminator == 'f':
                        cmd = CH+":TER "+"FIF"
                        self.Instrument.write(cmd)
                        pass
                else:
                        print("Wrong argument")
                pass
        
        def get_channel_input_terminator(self, CH):
                terminator = self.Instrument.ask(CH+":TER?")
                return terminator
        