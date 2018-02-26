#!/usr/bin/python3
#-*- codin: utf-8 -*-
import os, sys, csv
import numpy as np
from Units.Functions import *

class MeasurementData(csv):
        def __init__(self, filename):
                super(MeasurementData, self).__init__()
                self._data_set = [] # empty list
                self.fileName = filename # filename
                pass
        
        def set_data_arrays(self,R,S, *args):
                try:
                        time_array = args[0]
                        time_unit = args[1]
                        channel_one = args[2]
                        channel_two =args[3]
                        channel_as_current_density = getCurrentDensity(channel_two, R, S)
                        pass
                except Exception as ex:
                        print("FCUK")
                        print(str(ex))
                pass
        
        