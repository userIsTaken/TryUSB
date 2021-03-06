#!/usr/bin/python3
#-*- codin: utf-8 -*-
import os, sys, csv
from csv import writer
from PyQt5.QtCore import pyqtSignal, QObject

import traceback as tcb
import numpy as np
from Units.Functions import *
import itertools as itr

class MeasurementData(QObject):
        results = pyqtSignal(str)
        def __init__(self, filename):
                super(MeasurementData, self).__init__()
                self._data = None # empty
                self._header = None
                self._frow = None
                self._srow = None
                self.fileName = filename # filename
                pass
        
        def set_data_array(self,R,S, *args):
                '''

                :param R:
                :param S:
                :param args: 0 - time array, 1  - time unit, 2  - CH1, 3  - CH2, 4 - string containing generators info
                :return:
                '''
                try:
                        time_array = args[0]
                        time_unit = args[1]
                        measurement_parameters = args[4] # string containing generators info
                        channel_one = args[2]
                        channel_two =args[3]
                        channel_as_current_density = getCurrentDensity(channel_two, R, S)
                        self._header = ["?"+str(measurement_parameters)+"?", "Apkrovos varža R="+str(R)+" kΩ", "Kontakto plotas S="+str(S)+" cm^2", ""]
                        self._frow = ["t["+str(time_unit)+"]", "CH1/Signal", "CH2/Signal", "CH2/Density"]
                        self._srow = [str(time_unit), "V", "V", "mA/cm^2"]
                        self._data = itr.zip_longest(time_array, channel_one, channel_two, channel_as_current_density, fillvalue="-")
                        pass
                except Exception as ex:
                        err = tcb.format_exc()
                        self.results.emit("=====ERROR=====\n" + err)
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
                        err = tcb.format_exc()
                        self.results.emit("=====ERROR=====\n"+err)
                        pass
                pass

class DataArray(QObject):

        results = pyqtSignal(str)

        def __init__(self, *args, **kwargs):
                super(DataArray, self).__init__()
                self._list = [] # nested list/dictionary for all the data
                pass

        def append(self,R, S, **kwargs):
                '''

                :param R:
                :param S:
                :param kwargs: TIME, TIMEU, CHAN1, CHAN2, MPARAMS, NAME
                :return:
                '''
                time_array = kwargs["TIME"]
                time_unit = kwargs["TIMEU"]
                channel_one = kwargs["CHAN1"]
                channel_two = kwargs["CHAN2"]
                measurement_params = kwargs["MPARAMS"]
                name = kwargs["NAME"]
                ch2_density = getCurrentDensity(channel_two, R, S)
                _header = ["?" + str(measurement_params) + "?", "Apkrovos varža R="+str(R)+" kΩ", "Kontakto plotas S="+str(S)+" cm^2", ""]
                _frow = ["t[" + str(time_unit) + "]", "CH1/Signal", "CH2/Signal", "CH2/Density"]
                _srow = [str(time_unit), "V", "V", "mA/cm^2"]
                _data = itr.zip_longest(time_array, channel_one, channel_two, ch2_density,
                                             fillvalue="-")
                lst = {"NAME":name, "HEADER":_header, "FROW":_frow, "SROW":_srow, "DATA":_data}
                self._list.append(lst)
                pass

        def write_all_lists(self, fileNameAndPathModel):
                try:
                        if len(self._list) > 0:
                                for dct in self._list:
                                        with open(fileNameAndPathModel+dct["NAME"]+".csv", 'w', newline='') as csvfile:
                                                csvwriter = writer(csvfile, delimiter=';',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                                self.results.emit("Rašoma bus į failą: "+fileNameAndPathModel+dct["NAME"]+".csv")
                                                csvwriter.writerow(dct["HEADER"])
                                                csvwriter.writerow(dct["FROW"])
                                                csvwriter.writerow(dct["SROW"])
                                                for a in dct["DATA"]:
                                                        csvwriter.writerow(a)
                                                pass
                                        pass
                                pass
                        else:
                                self.results.emit("Zero length of dct")
                except Exception as ex:
                        err = tcb.format_exc()
                        self.results.emit("=====ERROR=====\n" + err)
                        print("FCUK AGAIN")
                        print(str(ex))