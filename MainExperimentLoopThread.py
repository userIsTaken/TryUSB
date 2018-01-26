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
                        timeOFF = self.kwargs['OFFtime']
                        timeU = self.kwargs['timeU']
                        i = 0
                        try:
                                while totalV <= stopV:
                                        self.Generator.SetAmplitude(self.Generator.CH1, totalV)
                                        self.Generator.SetPeriod(self.Generator.CH1, timeOFF, timeU, i)
                                        trigger = totalV / 4 + self.kwargs['fixedOFF']
                                        tr = str("{0:.2f}".format(trigger))
                                        print(tr, "tr")
                                        scale = totalV / 4
                                        sc = str("{0:.2f}".format(scale))
                                        self.Oscilograph.set_y_scale("CHAN1", sc)
                                        
                                        if ("uS" == timeU):
                                                t_u = str((timeOFF/4) * (10 ** -6))
                                                self.Oscilograph.set_time_scale(t_u)
                                                print("Periodas ", t_u)
                                                time.sleep(2.0)
                                                pass
                                        elif ("mS" == timeU):
                                                t_u = str((timeOFF/4) * (10 ** -3))
                                                self.Oscilograph.set_time_scale(t_u)
                                                print("Periodas ", t_u)
                                                time.sleep(2.0)
                                                pass
                                        elif ("S" == timeU):
                                                t_u = str(timeOFF/4)
                                                self.Oscilograph.set_time_scale(t_u)
                                                print("Periodas ", t_u)
                                                time.sleep(2.0)
                                                pass
                                        else:
                                                pass
                                        
                                        self.Oscilograph.set_trigger_edge_level(tr)
                                        time.sleep(3.0)
                                        
                                        data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel("CHAN1")
                                        time.sleep(1.0)
                                        data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel("CHAN2")
                                        self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(), time_array.tolist(), time_unit)
                                        time.sleep(5.0)
                                        print("measured at ", totalV)
                                        totalV = totalV + stepV
                                        pass
                        except Exception as ex:
                                print(ex)
                                pass
                        finally:
                                self.final.emit(42)
                        pass
                                
                elif self.kwargs['key'] == 2:
                        self.Generator.SetAmplitude(self.Generator.CH1, self.kwargs['fixedV'])
                        startOFF = self.kwargs['startOFF']
                        stopOFF = self.kwargs['stopOFF']
                        totalOFF = startOFF
                        stepOFF = self.kwargs['stepOFF']
                        timeOFF = self.kwargs['OFFtime']
                        timeU = self.kwargs['timeU']
                        i = 0
                        try:
                                while totalOFF <= stopOFF:
                                        self.Generator.SetOffset(self.Generator.CH1, totalOFF)
                                        self.Generator.SetPeriod("CH1", timeOFF, timeU)
                                        trigger = totalOFF + self.kwargs['fixedV'] / 4
                                        tr = str("{0:.2f}".format(trigger))
                                        print(tr, "tr")
                                        scale = self.kwargs['fixedV'] / 4
                                        sc = str("{0:.2f}".format(scale))
                                        self.Oscilograph.set_y_scale("CHAN1", sc)
                                        self.Oscilograph.set_trigger_edge_level(tr)
                                        time.sleep(3.0)
                        
                                        data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel(
                                                "CHAN1")
                                        data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                "CHAN2")
                                        self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(),
                                                          time_array.tolist(), time_unit)
                                        time.sleep(5.0)
                                        print("measured at ", totalOFF)
                                        totalOFF = totalOFF + stepOFF
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
                else:
                        pass
                
                # self.deleteLater()