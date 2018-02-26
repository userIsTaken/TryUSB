#!/usr/bin/python3
#-*- codin: utf-8 -*-
import os, sys, csv
import numpy as np


class MeasurementData(csv):
        def __init__(self, filename):
                super(MeasurementData, self).__init__()
                self._data_set = [] # empty list
                self.fileName = filename # filename
                pass
        
        def set_data_arrays(self, *args):
                try:
                        pass
                except Exception as ex:
                        print("FCUK")
                        print(str(ex))
                pass
        
        