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

        def write(self, command):
                """Send an arbitrary command directly to the scope"""
                self.Instrument.write(command)
                pass

        def read(self, command):
                """Read an arbitrary amount of data directly from the scope"""
                answer = self.Instrument.ask(command)
                return answer
                pass

        
        def reset(self):
                pass

        def close(self):
                pass

        def stop(self):
                pass

        def channels_mode(self, mode: str = "NORM"):
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
        
        