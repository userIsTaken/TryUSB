from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
from Units.LimitsCheck import check_y_scale
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
                self._require_stop = False
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
                                i = 0
                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                self.Generator.SetPeriod(self.Generator.CH1, timeOFF, time_u, i)
                                self.AMP_OSC_time_scale_and_offset(timeOFF, time_u)
                                try:
                                        print("try fork:")
                                        while ((totalV <= stopV) and (not self._require_stop)):
                                                self.AMP_GEN_set_parameters(totalV, fixed_offset)
                                                
                                                self.AMP_OSC_set_parameters(self.Oscilograph.CH1, totalV, fixed_offset)
                                                
                                                self.Generator.EnableOutput(self.Generator.CH1, ON)
                                                signal_wait = self.Generator.GetTriggerInterval()
                                                print("what?")
                                                
                                                if ("uS" == time_u):
                                                        t_u = (timeOFF) * (10 ** -6)
                                                        print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                elif ("mS" == time_u):
                                                        t_u = (timeOFF) * (10 ** -3)
                                                        print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                elif ("S" == time_u):
                                                        t_u = timeOFF
                                                        print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                print("data scanning ...")
                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                        self.Oscilograph.CH2)
                                                print("kreipimasis", time_unit2)
                                                change, max_y = check_y_scale(data_from_channel2)
                                                print("max y", max_y, "change", str(change))
                                                if change is True:
                                                        while change is True:
                                                                self.AMP_OSC_set_parameters(self.Oscilograph.CH2, max_y * 2,
                                                                                            (max_y*2 + fixed_offset) / 8)
                                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                                        "CHAN2")
                                                                change, max_y = check_y_scale(data_from_channel2)
                                                                if change is False:
                                                                        self.AMP_OSC_set_parameters(
                                                                                self.Oscilograph.CH2,
                                                                                max_y, (max_y + fixed_offset)/8)
                                                                pass
                                                elif change is False:
                                                        self.AMP_OSC_set_parameters(
                                                                self.Oscilograph.CH2,
                                                                max_y, (max_y + fixed_offset) / 8)
                                                
                                                self.OSC_read()
                                                self.progress.emit("measured at " + str(totalV))
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
                                        while totalOFF <= stopOFF and not self._require_stop:
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
                                                self.OSC_read()
                                                # data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel(
                                                #         "CHAN1")
                                                # data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                #         "CHAN2")
                                                # self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(),
                                                #                   time_array.tolist(), time_unit)
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
                                self.progress.emit("Else fork, stopping ... ")
                                # TODO we need to describe all variants who can occur in if conditions
                                # sys.exit(-1)
                except Exception as ex:
                        self.progress.emit(str(ex))
                        self.errors.emit(-1, str(ex))
                        # sys.exit(-1)
                        pass
                finally:
                        self.progress.emit("Pabaiga")
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
        
        def AMP_OSC_time_scale_and_offset(self, signal_t, unit):
                if ("uS" == unit):
                        t_u = (signal_t / 8) * (10 ** -6)
                        self.Oscilograph.set_closest_time_scale(signal_t / 8, unit)
                        time.sleep(1)
                        self.Oscilograph.set_time_offset(str("{0:.8f}".format(-t_u * 4)))
                        self.progress.emit("Periodas " + str("{0:.8f}".format(t_u)))
                        # time.sleep(wait_pls)
                        pass
                elif ("mS" == unit):
                        t_u = (signal_t / 8) * (10 ** -3)
                        self.Oscilograph.set_closest_time_scale(signal_t / 8, unit)
                        time.sleep(1)
                        self.Oscilograph.set_time_offset(str("{0:.8f}".format(-t_u * 4)))
                        self.progress.emit("Periodas " + str("{0:.8f}".format(t_u)))
                        pass
                elif ("S" == unit):
                        t_u = signal_t / 8
                        self.Oscilograph.set_closest_time_scale(signal_t / 8, unit)
                        time.sleep(1)
                        self.Oscilograph.set_time_offset(str("{0:.8f}".format(-t_u * 4)))
                        self.progress.emit("Periodas " + str("{0:.8f}".format(t_u)))
                        pass
                else:
                        self.progress.emit("shit here")
                        pass
                pass
        
        def OSC_read(self):
                data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel(
                        "CHAN1")
                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                        "CHAN2")
                self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(),
                                  time_array.tolist(), time_unit)
                pass
        
        def AMP_GEN_set_parameters(self, amplitude, fixed_offset):
                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                time.sleep(0.1)
                self.Generator.SetAmplitude(self.Generator.CH1, amplitude)
                time.sleep(0.1)
                offset = self.GetOffset(amplitude, fixed_offset)
                self.Generator.SetOffset(self.Generator.CH1, offset)
                pass
        
        def AMP_OSC_set_parameters(self, CH,  amplitude, fixed_offset=0):
                scale = (amplitude + fixed_offset) / 6
                sc = str("{0:.2f}".format(scale))
                self.Oscilograph.set_y_scale(CH, sc)
                trigger = (amplitude) / 4 + fixed_offset
                tr = str("{0:.2f}".format(trigger))
                time.sleep(1)
                self.Oscilograph.set_trigger_edge_level(tr)
                # print(tr, "tr")
                self.progress.emit(str(tr) + " tr")
        
                time.sleep(1)
                self.Oscilograph.set_channel_offset(CH,
                                                    str(-3.0 * scale))
                time.sleep(1)  # 100 ms is enough
                pass

        @pyqtSlot()
        def stop(self):
                print("measurement thread will stop anytime soon")
                self._require_stop = True
                pass
