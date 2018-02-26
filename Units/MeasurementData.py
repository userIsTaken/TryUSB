#!/usr/bin/python3
#-*- codin: utf-8 -*-
import os, sys, csv
from csv import writer

import numpy as np
from Units.Functions import *
import itertools as itr

class MeasurementData():
        def __init__(self, filename):
                super(MeasurementData, self).__init__()
                self._data = None # empty
                self._header = None
                self._frow = None
                self._srow = None
                self.fileName = filename # filename
                pass
        
        def set_data_array(self,R,S, *args):
                try:
                        time_array = args[0]
                        time_unit = args[1]
                        measurement_parameters = args[4] # string containing generators info
                        channel_one = args[2]
                        channel_two =args[3]
                        channel_as_current_density = getCurrentDensity(channel_two, R, S)
                        self._header = "?HEADER?\n"+str(measurement_parameters)+"\n"
                        self._frow = ["t["+str(time_unit)+"]", "CH1/Signal", "CH2/Signal", "CH2/Density"]
                        self._srow = [str(time_unit), "V", "V", "A/cm^2"]
                        self._data = itr.zip_longest(time_array, channel_one, channel_two, channel_as_current_density, fillvalue="-")
                        pass
                except Exception as ex:
                        print("FCUK")
                        print(str(ex))
                pass
        
        def write_to_file(self):
                try:
                        with open(self.fileName, 'w', newline='') as csvfile:
                                wrt = writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                wrt.writerow(self._header)
                                wrt.writerow(self._frow)
                                wrt.writerow(self._srow)
                                for row in self._data:
                                        wrt.writerow(row)
                                pass
                        pass
                except Exception as ex:
                        print("==================")
                        print(str(ex))
                        print("==================")
                        pass
                pass
        
        