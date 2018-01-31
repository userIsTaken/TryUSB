from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time
# from DummyFiles.DummyFunctions import *
ON = "ON"
OFF = "OFF"
class LoopWorker(QObject):
        results = pyqtSignal(list, list, list, str)
        errors = pyqtSignal(int, str)
        final = pyqtSignal(int)
        progress = pyqtSignal(str)
        
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
                                # self.Generator.SetOffset(self.Generator.CH1, self.kwargs['fixedOFF'])
                                # self.Oscilograph.set_channel_offset(self.Oscilograph.CH1, "-2")
                                startV = self.kwargs['startV']
                                stopV = self.kwargs['stopV']
                                totalV = startV
                                stepV = self.kwargs['stepV']
                                timeOFF = self.kwargs['OFFtime']
                                time_u = self.kwargs['timeU']
                                fixed_offset = self.kwargs['fixedOFF']
                                wait_pls = 0
                                i = 0
                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                self.Generator.SetPeriod(self.Generator.CH1, timeOFF, time_u, i)
                                try:
                                        while totalV <= stopV:
                                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                                time.sleep(0.1)
                                                self.Generator.SetAmplitude(self.Generator.CH1, totalV)
                                                time.sleep(0.1)
                                                offset = self.GetOffset(totalV, fixed_offset)
                                                self.Generator.SetOffset(self.Generator.CH1, offset)
                                                trigger = (totalV) / 4 + fixed_offset
                                                tr = str("{0:.2f}".format(trigger))
                                                # print(tr, "tr")
                                                self.progress.emit(str(tr)+" tr")
                                                scale = (totalV+fixed_offset) / 4
                                                sc = str("{0:.2f}".format(scale))
                                                time.sleep(1)
                                                self.Oscilograph.set_y_scale(self.Oscilograph.CH1, sc)
                                                time.sleep(2) # 100 ms is enough
                                                if ("uS" == time_u):
                                                        t_u = (timeOFF / 4) * (10 ** -6)
                                                        self.Oscilograph.set_time_scale(str("{0:.8f}".format(t_u)))
                                                        self.progress.emit("Periodas " + str("{0:.8f}".format(t_u)))
                                                        wait_pls = float(timeOFF) * 2.1
                                                        self.progress.emit("Laukiam " + str( wait_pls))
                                                        self.Oscilograph.set_trigger_edge_level(tr)
                                                        # time.sleep(wait_pls)
                                                        pass
                                                elif ("mS" == time_u):
                                                        t_u = str((timeOFF / 4) * (10 ** -3))
                                                        self.Oscilograph.set_time_scale(t_u)
                                                        self.progress.emit("Periodas "+ str( t_u))
                                                        wait_pls = float(timeOFF) * 2.1
                                                        self.progress.emit("Laukiam " + str( wait_pls))
                                                        self.Oscilograph.set_trigger_edge_level(tr)
                                                        # time.sleep(wait_pls)
                                                        pass
                                                elif ("S" == time_u):
                                                        t_u = str(timeOFF / 4)
                                                        self.Oscilograph.set_time_scale(t_u)
                                                        self.progress.emit("Periodas " + str( timeOFF))
                                                        # self.Oscilograph.set_trigger_edge_level(tr)
                                                        wait_pls = float(timeOFF) * 2.1
                                                        self.progress.emit("Laukiam " + str( wait_pls))
                                                        self.Oscilograph.set_trigger_edge_level(tr)
                                                        # time.sleep(wait_pls)
                                                        pass
                                                else:
                                                        self.progress.emit("shit here")
                                                        pass
                                                time.sleep(1)
                                                self.Generator.EnableOutput(self.Generator.CH1, ON)
                                                self.Oscilograph.set_channel_offset(self.Oscilograph.CH1,str(-1.0 * fixed_offset))
                                                self.Oscilograph.unlock_key()
                                                self.progress.emit("Wait 20 s")
                                                time.sleep(20)
                                                data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel("CHAN1")
                                                time.sleep(0.1)
                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel("CHAN2")
                                                self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(), time_array.tolist(), time_unit)
                                                time.sleep(2.0) # 2.0 seconds are enough
                                                self.progress.emit("measured at " + str( totalV))
                                                totalV = totalV + stepV
                                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                                self.Oscilograph.unlock_key()
                                                pass
                                except Exception as ex:
                                        print(ex)
                                        self.errors.emit(-1, str(ex)+" " + ex.args)

                        elif self.kwargs['key'] == 2:
                                fixedAmpl = self.kwargs['fixedV']
                                self.Generator.SetAmplitude(self.Generator.CH1, fixedAmpl)
                                startOFF = self.kwargs['startOFF']
                                stopOFF = self.kwargs['stopOFF']
                                totalOFF = startOFF
                                stepOFF = self.kwargs['stepOFF']
                                timeOFF = self.kwargs['OFFtime']
                                i = 0
                                try:
                                        while totalOFF <= stopOFF:
                                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                                time.sleep(1)
                                                self.Generator.SetNormalizedOffset(self.Generator.CH1, totalOFF, float(fixedAmpl))
                                                trigger = totalOFF + fixedAmpl / 4
                                                tr = str("{0:.2f}".format(trigger))
                                                print(tr, "tr")
                                                scale = fixedAmpl / 4
                                                sc = str("{0:.2f}".format(scale))
                                                self.Oscilograph.set_y_scale("CHAN1", sc)
                                                time.sleep(1)
                                                self.Oscilograph.set_trigger_edge_level(tr)
                                                time.sleep(3.0)
                                                self.Oscilograph.set_channel_offset(self.Oscilograph.CH1, str(-1*totalOFF))
                                                time.sleep(3.0)
                                                self.Generator.EnableOutput(self.Generator.CH1, ON)
                                                time.sleep(2.0)
                                                data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel(
                                                        "CHAN1")
                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                        "CHAN2")
                                                self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(),
                                                                  time_array.tolist(), time_unit)
                                                time.sleep(5.0)
                                                print("measured at ", totalOFF)
                                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                                self.Oscilograph.unlock_key()
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
                        self.errors.emit(-1, str(ex))
                        # sys.exit(-1)
                        pass
                finally:
                        self.final.emit(42)
                        pass
                
                # self.deleteLater()
                
        def GetOffset(self, ampl, offs):
                '''
                
                :param ampl:
                :param offs:
                :return:
                '''
                
                really_good_offset = ampl/2 + offs
                return really_good_offset
                
                pass
