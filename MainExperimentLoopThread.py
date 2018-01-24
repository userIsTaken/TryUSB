from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time
# from DummyFiles.DummyFunctions import *

class LoopWorker(QObject):
        results = pyqtSignal(list, list, list, str)
        errors = pyqtSignal(int, str)
        final = pyqtSignal(int)
        
        def __init__(self, generator, oscilograph, *args, **kwargs):
                super(LoopWorker, self).__init__()
                # QThread().__init__(self)
                self.Generator = generator
                self.Oscilograph = oscilograph
                self.args = args
                self.kwargs = kwargs
                # self.start() # WHY?????
                print("Init")
                pass


        @pyqtSlot()
        def run(self):
                print("Try to run this stuff")
                # TODO it seems that this logic is wrong. 
                if self.kwargs['key'] == 1:
                        self.Generator.SetOffset(self.Generator.CH1, self.kwargs['fixedOFF'])
                        startV = self.kwargs['startV']
                        stopV = self.kwargs['stopV']
                        totalV = startV
                        stepV = self.kwargs['stepV']
                i = 0
                try:
                        while totalV <= stopV:
                                self.Generator.SetAmplitude(self.Generator.CH1, totalV)
                                data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel("CHAN1")
                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel("CHAN2")
                                self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(), time_array.tolist(), time_unit)
                                time.sleep(2)
                                totalV += stepV
                                print("measured at ", totalV)
                                pass
                        # while i <= 15:
                                # print("?????", i)
                                # # setting parameters:
                                # if self.kwargs["key"] is 1:
                                #
                                #         pass
                                #
                                # # result = self.fn(str(self.args[0]))
                                # data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel("CHAN1")
                                # data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel("CHAN2")
                                # # print(result)
                                # self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(), time_array.tolist(), time_unit)
                                # time.sleep(2)
                                # i = i+1
                                # pass
                        # self.final.emit(42)
                except Exception as ex:
                        print(ex)
                        pass
                finally:
                        self.final.emit(42)
                pass
