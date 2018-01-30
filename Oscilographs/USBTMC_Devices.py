# for file access
import os
# for timed waits
import time
import numpy as np

class USBTMC:
        """
        Very Simple usbmtc device
        """
        def __init__(self, device):
                self.device = device
                self.FILE = os.open(device, os.O_RDWR)

        def write(self, command):
                os.write(self.FILE, str.encode(command))

        def read(self, length=4000):
                '''
                
                :param length: length of data to raed
                :return:
                '''
                return os.read(self.FILE, length)

        def getName(self):
                self.write("*IDN?")
                return self.read(300)

        def sendReset(self):
                self.write("*RST")

        def closeDevice(self):
                os.close(self.FILE)



class SimpleInstrument:
        '''
        Simpe class useful to test a basic functions. It supports write, read, getName, reset functions;
        '''

        def __init__(self, device):
                self.meas = USBTMC(device)

        def write(self, command):
                """Send an arbitrary command directly to the scope"""
                self.meas.write(command)

        def read(self, length):
                """Read an arbitrary amount of data directly from the scope
                
                :param length: length of data to read
                """
                return self.meas.read(length)

        def getName(self):
                return self.meas.getName()

        def reset(self):
                """Reset the instrument"""
                self.meas.sendReset()

        def close(self):
                self.meas.closeDevice()

class RigolDS1000SeriesScope:
        def __init__(self, device):
                self.meas = USBTMC(device)
                self.CH1 = "CHAN1"
                self.CH2 = "CHAN2"
                # Initialization part
        def write(self, command):
                """Send an arbitrary command directly to the scope"""
                self.meas.write(command)

        def read(self, command):
                """Read an arbitrary amount of data directly from the scope"""
                return self.meas.read(command)

        def get_name(self):
                return self.meas.getName()

        def reset(self):
                """Reset the instrument"""
                self.meas.sendReset()

        def close(self):
                self.meas.closeDevice()
        
        def stop(self):
                self.meas.write(":STOP")
                
        def channels_mode(self, mode:str="NORM"):
                '''
                Sets mode for CHAN1 and CHAN2
                
                :param str mode: NORM, RAW, MAX
                :return:
                '''
                self.meas.write(":WAV:POIN:MODE "+mode)
                
        def get_channels_mode(self):
                '''
                function returns wave mode for all channels
                :return:
                '''
                self.write(":WAV:POIN:MODE?")
                time.sleep(0.1) # sleep for 100 ms;
                answer=self.read(9000)
                return answer
        
        def get_data_from_channel(self, channel, length=9000):
                '''
                Get arbitrary amount of data from specified channel
                
                :param str channel: CHAN1, CHAN2
                :param int length: default 9000
                :return array: array of data, already converted from binary form
                '''
                self.write(":WAV:DATA? "+channel)
                dataFromBuffer = self.read(length)
                data = np.frombuffer(dataFromBuffer, 'B')
                #:CHANnel < n >: SCALe < range >
                return data
                
        def get_channel_scale(self, CH:str):
                '''
                # Get the voltage scale CH1
                
                :return: voltscaleCH1 in Volts?
                '''
                self.write(":"+CH+":SCAL?")
                voltscaleCH = float(self.read(20))
                return voltscaleCH
        
        def get_channel_CHAN2_scale(self):
                '''
                # Get the voltage scale CH2
                
                :return: voltscaleCH2 in Volts?
                '''
                self.write(":CHAN2:SCAL?")
                voltscaleCH2 = float(self.read(20))
                return voltscaleCH2
        
        def get_time_scale(self):
                '''
                Get time scale
                # TIME SECTION ===========================
                # Get the timescale
                
                :return:
                '''
                self.write(":TIM:SCAL?")
                timescale = float(self.read(20))
                return timescale
        
        def get_time_offset(self):
                '''
                # Get the timescale offset
                :return:
                '''
                self.write(":TIM:OFFS?")
                timeoffset = float(self.read(20))
                return timeoffset

        def get_time_array(self, dataCHANNEL):
                '''

                :param array dataCHANNEL: array of data from channel
                :return: time, time Unit - time array and time dimension
                '''
                timescale = self.get_time_scale()
                # Now, generate a time axis.  The scope display range is 0-600, with 300 being
                # time zero.
                time = np.arange(-300.0 / 50 * timescale, 300.0 / 50 * timescale, timescale / 50.0)
        
                # If we generated too many points due to overflow, crop the length of time.
                if (time.size > dataCHANNEL.size):
                        time = time[0:600:1]  # need to adopt to my needs.
                elif (time.size < dataCHANNEL.size):
                        dataCHANNEL = dataCHANNEL[0:600:1]
                        pass
                else:
                        pass
                # tUnit section:
                if (time[599] < 1e-3):
                        time = time * 1e6
                        tUnit = "uS"
                elif (time[599] < 1):
                        time = time * 1e3
                        tUnit = "mS"
                else:
                        tUnit = "S"
        
                return time, tUnit, dataCHANNEL
        
        def get_channel_offset(self, CHANNEL):
                '''
                This function returns offset of specified channel
                
                :param str CHANNEL: channel
                :return:
                '''
                self.write(":"+CHANNEL+":OFFS?")
                voltoffsetCH = float(self.read(20))
                return voltoffsetCH
        
        def set_channel_offset(self, CHANNEL, OFFset:str):
                self.write(":" + CHANNEL + ":OFFS " + OFFset)
                pass
        
        def get_data_points_from_channel(self, CH: str):
                '''

                :param str CH: channel
                :return: dataCH1, time_array, time_unit
                '''
                # Stop data acquisition:
                self.stop()
                # set wave data points mode to normal:
                self.channels_mode("NORM")
                data_array_from_channel = self.get_data_from_channel(CH, 9000)
                # Walk through the data, and map it to actual voltages
                # First invert the data (ya rly)
                dataCH = data_array_from_channel * -1 + 255
                # Voltage scale:
                voltscaleCH = self.get_channel_scale(CH)
                # Voltage offset
                voltoffsetCH = self.get_channel_offset(CH)
                # Now, we know from experimentation that the scope display range is actually
                # 30-229.  So shift by 130 - the voltage offset in counts, then scale to
                # get the actual voltage.
                dataCH1 = (dataCH - 130.0 - voltoffsetCH / voltscaleCH * 25) / 25 * voltscaleCH
                # ==========================
                # Get a time scale:
                time_scale = self.get_time_scale()
                # get a time offset:
                time_offset = self.get_time_offset()
                # get time array:
                time_array, time_unit, dataCH2 = self.get_time_array(dataCH1)
                self.run()
                self.unlock_key()
                return dataCH2, time_array, time_unit
                pass

        def run(self):
                self.write(":RUN")
                pass

        def unlock_key(self):
                self.write(":KEY:FORC")
                pass
        
        def set_y_scale(self, CHAN, y_scale:str, sleep_time = 0.5):
                '''

                :param CHAN: channel CHAN1, CHAN2
                :param y_scale: volts
                :return:
                '''

                #self.write(":CHAN1:PROB 1")
                self.write(":"+CHAN+":SCAL "+y_scale)
                time.sleep(sleep_time)
                pass
        
        def set_time_scale(self, time_scale:str, sleep_time=0.5):
                '''

                :param str time_scale: time scale in seconds
                :return:
                '''
                self.write(":TIM:SCAL "+ time_scale)
                time.sleep(sleep_time)
                pass

        def set_trigger_edge_level(self, level:str):
                '''

                :param level: trigger level
                :return:
                '''

                self.write(":TRIG:EDGE:LEV "+level)
                pass