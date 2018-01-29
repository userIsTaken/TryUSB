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
                self.Generator = generator
                self.Oscilograph = oscilograph
                self.args = args
                self.kwargs = kwargs
                print("Init")
                pass


        @pyqtSlot()
        def run(self):
                try:
                        print("Try to run this stuff")
                        if self.kwargs['key'] == 1:
                                self.Generator.SetOffset(self.Generator.CH1, self.kwargs['fixedOFF'])
                                self.Oscilograph.set_channel_offset(self.Oscilograph.CH1, "-2")
                                startV = self.kwargs['startV']
                                stopV = self.kwargs['stopV']
                                totalV = startV
                                stepV = self.kwargs['stepV']
                                timeOFF = self.kwargs['OFFtime']
                                time_u = self.kwargs['timeU']
                                i = 0
                                try:
                                        while totalV <= stopV:
                                                self.Generator.SetAmplitude(self.Generator.CH1, totalV)
                                                trigger = (totalV + self.kwargs['fixedOFF']) / 4
                                                tr = str("{0:.2f}".format(trigger))
                                                print(tr, "tr")
                                                scale = totalV / 4
                                                sc = str("{0:.2f}".format(scale))
                                                self.Generator.SetPeriod(self.Generator.CH1, timeOFF, time_u, i)
                                                time.sleep(1)
                                                self.Oscilograph.set_y_scale("CHAN1", sc)
                                                time.sleep(1) # 100 ms is enough
                                                
                                                
                                                if ("uS" == time_u):
                                                        t_u = (timeOFF / 4) * (10 ** -6)
                                                        self.Oscilograph.set_time_scale(str("{0:.8f}".format(t_u)))
                                                        print("Periodas ", str("{0:.8f}".format(t_u)))
                                                        wait_pls = float(timeOFF) * 2.1
                                                        print("Laukiam ", wait_pls)
                                                        self.Oscilograph.set_trigger_edge_level(tr)
                                                        time.sleep(wait_pls)
                                                        pass
                                                elif ("mS" == time_u):
                                                        t_u = str((timeOFF / 4) * (10 ** -3))
                                                        self.Oscilograph.set_time_scale(t_u)
                                                        print("Periodas ", t_u)
                                                        wait_pls = float(timeOFF) * 2.1
                                                        print("Laukiam ", wait_pls)
                                                        self.Oscilograph.set_trigger_edge_level(tr)
                                                        time.sleep(wait_pls)
                                                        pass
                                                elif ("S" == time_u):
                                                        t_u = str(timeOFF / 4)
                                                        self.Oscilograph.set_time_scale(t_u)
                                                        print("Periodas ", timeOFF)
                                                        # self.Oscilograph.set_trigger_edge_level(tr)
                                                        wait_pls = float(timeOFF) * 2.1
                                                        print("Laukiam ", wait_pls)
                                                        self.Oscilograph.set_trigger_edge_level(tr)
                                                        time.sleep(wait_pls)
                                                        pass
                                                else:
                                                        print("shit here")
                                                        pass
                                                data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel("CHAN1")
                                                time.sleep(0.1)
                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel("CHAN2")
                                                self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(), time_array.tolist(), time_unit)
                                                time.sleep(2.0) # 2.0 seconds are enough
                                                print("measured at ", totalV)
                                                totalV = totalV + stepV
                                                pass
                                except Exception as ex:
                                        print(ex)
                                        self.errors.emit(-1, str(ex)+" " + ex.args)
                                        # self.deleteLater()
                                        # sys.exit(-1)

                        elif self.kwargs['key'] == 2:
                                self.Generator.SetAmplitude(self.Generator.CH1, self.kwargs['fixedV'])
                                startOFF = self.kwargs['startOFF']
                                stopOFF = self.kwargs['stopOFF']
                                totalOFF = startOFF
                                stepOFF = self.kwargs['stepOFF']
                                timeOFF = self.kwargs['OFFtime']
                                i = 0
                                try:
                                        while totalOFF <= stopOFF:
                                                self.Generator.SetOffset(self.Generator.CH1, totalOFF)
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

                                except Exception as ex:
                                        print(ex)
                                        self.errors.emit(-1, str(ex) + " " + ex.args)
                                        # sys.exit(-1)
                        else:
                                print("Else fork, stopping ... ")
                                # TODO we need to describe all variants who can occur in if conditions
                                # sys.exit(-1)
                except Exception as ex:
                        print(ex)
                        self.errors.emit(-1, str(ex) + " " + ex.args)
                        # sys.exit(-1)
                        pass
                finally:
                        self.final.emit(42)
                        pass
                
                # self.deleteLater()
