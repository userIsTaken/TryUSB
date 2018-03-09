from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
from Units.LimitsCheck import check_y_scale
import time
# from DummyFiles.DummyFunctions import *
ON = "ON"
OFF = "OFF"

import traceback

class LoopWorker(QObject):
        results = pyqtSignal(list, list, list, str, dict)
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
                self.Oscilograph.cmd_emiter.connect(self.emit_str)
                #
                self._measurement_parameters = {}
                self._current_ampl = 0
                self._current_offs = 0
                self._current_period = 0
                self._current_time_unit = ""
                #print("Init")
                pass
        
        def emit_str(self, string):
                self.progress.emit(string)
                pass

        @pyqtSlot()
        def run(self):
                try:
                        #print("Try to run this stuff")
                        if self.kwargs['key'] == 1:
                                # self.Generator.SetOffset(self.Generator.CH1, self.kwargs['fixedOFF'])
                                # self.Oscilograph.set_channel_position(self.Oscilograph.CH1, "-2")
                                startV = self.kwargs['startV']
                                stopV = self.kwargs['stopV']
                                totalV = startV
                                stepV = self.kwargs['stepV']
                                timeOFF = self.kwargs['OFFtime']
                                time_u = self.kwargs['timeU']
                                fixed_offset = self.kwargs['fixedOFF']
                                self._current_offs = fixed_offset
                                self._current_period = timeOFF
                                self._current_time_unit = time_u
                                i = 0
                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                self.Generator.SetPeriod(self.Generator.CH1, timeOFF, time_u, i)
                                self.AMP_OSC_time_scale_and_offset(timeOFF, time_u)
                                try:
                                        #print("try fork:")
                                        while ((totalV <= stopV) and (not self._require_stop)):
                                                self.AMP_GEN_set_parameters(totalV, fixed_offset)
                                                self._current_ampl = totalV
                                                self.AMP_OSC_set_parameters(self.Oscilograph.signalChannel, totalV, fixed_offset)
                                                
                                                self.Generator.EnableOutput(self.Generator.CH1, ON)
                                                signal_wait = self.Generator.GetTriggerInterval()
                                                #print("what?")
                                                
                                                if ("uS" == time_u):
                                                        t_u = (timeOFF) * (10 ** -6)
                                                        #print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                elif ("mS" == time_u):
                                                        t_u = (timeOFF) * (10 ** -3)
                                                        #print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                elif ("S" == time_u):
                                                        t_u = timeOFF
                                                        #print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                #print("data scanning ...")
                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                        self.Oscilograph.responseChannel)
                                                #print("kreipimasis", time_unit2)
                                                change, max_y = check_y_scale(data_from_channel2)
                                                #print("max y", max_y, "change", str(change))
                                                if change is True:
                                                        while change is True:
                                                                self.AMP_OSC_set_parameters(self.Oscilograph.responseChannel, max_y * 2)
                                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                                        self.Oscilograph.responseChannel)
                                                                change, max_y = check_y_scale(data_from_channel2)
                                                                if change is False:
                                                                        self.AMP_OSC_set_parameters(
                                                                                self.Oscilograph.responseChannel,
                                                                                max_y)
                                                                pass
                                                elif change is False:
                                                        self.AMP_OSC_set_parameters(
                                                                self.Oscilograph.responseChannel,
                                                                max_y)
                                                time.sleep(2)
                                                self.OSC_read()
                                                self.progress.emit("measured at " + str(totalV))
                                                totalV = totalV + stepV
                                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                                self.Oscilograph.unlock_key()
                                                pass
                                except Exception as ex:
                                        #print(ex)
                                        self.errors.emit(-1, str(ex)+" " + ex.args)

                        elif self.kwargs['key'] == 2:
                                fixedV = self.kwargs['fixedV']
                                startOFF = self.kwargs['startOFF']
                                stopOFF = self.kwargs['stopOFF']
                                totalOFF = startOFF
                                stepOFF = self.kwargs['stepOFF']
                                timeOFF = self.kwargs['OFFtime']
                                time_u = self.kwargs['timeU']
                                # info for data savings
                                # self._current_offs = fixed_offset
                                self._current_period = timeOFF
                                self._current_time_unit = time_u
                                self._current_ampl = fixedV
                                i = 0
                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                self.Generator.SetPeriod(self.Generator.CH1, timeOFF, time_u, i)
                                self.AMP_OSC_time_scale_and_offset(timeOFF, time_u)
                                try:
                                        #print("try fork:")
                                        while ((totalOFF <= stopOFF) and (not self._require_stop)):
                                                print("ciklas prasidejo")
                                                self._current_offs = totalOFF
                                                self.OFF_GEN_set_parameters(fixedV, totalOFF)
                
                                                self.AMP_OSC_set_parameters(self.Oscilograph.signalChannel, fixedV, totalOFF)
                
                                                self.Generator.EnableOutput(self.Generator.CH1, ON)
                                                signal_wait = self.Generator.GetTriggerInterval()
                                                #print("what?")
                
                                                if ("uS" == time_u):
                                                        t_u = (timeOFF) * (10 ** -6)
                                                        #print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                elif ("mS" == time_u):
                                                        t_u = (timeOFF) * (10 ** -3)
                                                        #print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                elif ("S" == time_u):
                                                        t_u = timeOFF
                                                        #print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                #print("data scanning ...")
                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                        self.Oscilograph.responseChannel)
                                                #print("kreipimasis", time_unit2)
                                                change, max_y = check_y_scale(data_from_channel2)
                                                #print("max y", max_y, "change", str(change))
                                                if change is True:
                                                        while change is True:
                                                                self.AMP_OSC_set_parameters(self.Oscilograph.responseChannel,
                                                                                            max_y * 2, totalOFF)
                                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                                        self.Oscilograph.responseChannel)
                                                                change, max_y = check_y_scale(data_from_channel2)
                                                                if change is False:
                                                                        self.AMP_OSC_set_parameters(
                                                                                self.Oscilograph.responseChannel,
                                                                                max_y, totalOFF)
                                                                pass
                                                elif change is False:
                                                        self.AMP_OSC_set_parameters(
                                                                self.Oscilograph.responseChannel,
                                                                max_y, totalOFF)
                
                                                self.OSC_read()
                                                self.progress.emit("measured at " + str(totalOFF))
                                                totalOFF = totalOFF + stepOFF
                                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                                self.Oscilograph.unlock_key()
                                                time.sleep(2)
                                                pass
                                except Exception as ex:
                                        #print(ex)
                                        self.errors.emit(-1, str(ex) + " " + str(ex.args))
                        elif self.kwargs['key'] == 3:  # time sweep
                                # self.Generator.SetOffset(self.Generator.CH1, self.kwargs['fixedOFF'])
                                # self.Oscilograph.set_channel_position(self.Oscilograph.CH1, "-2")
                                startT = self.kwargs['startT']
                                stopT = self.kwargs['stopT']
                                totalT = startT
                                stepT = self.kwargs['stepT']
                                fixedV = self.kwargs['fixedV']
                                time_u = self.kwargs['timeU']
                                fixed_offset = self.kwargs['fixedOFF']
                                self._current_offs = fixed_offset
                                # self._current_period = totalT
                                self._current_time_unit = time_u
                                self._current_ampl = fixedV
                                i = 0
                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                self.Generator.SetPeriod(self.Generator.CH1, totalT, time_u, i)
                                self.AMP_OSC_time_scale_and_offset(totalT, time_u)
                                self.AMP_GEN_set_parameters(fixedV, fixed_offset)
                                # self._current_ampl = fixedV
                                try:
                                        # print("try fork:")
                                        while ((totalT <= stopT) and (not self._require_stop)):
                                                self._current_period = totalT
                                                if (totalT <= stopT):
                                                        print("DEBUG: totalT, stopT", totalT, stopT)
                                                self.Generator.SetPeriod(self.Generator.CH1, totalT, time_u, i)
                                                
                                                time.sleep(1)
                                                self.AMP_OSC_set_parameters(self.Oscilograph.signalChannel, fixedV, fixed_offset)
                                                self.AMP_OSC_time_scale_and_offset(totalT, time_u)
                                                self.Generator.EnableOutput(self.Generator.CH1, ON)
                                                signal_wait = self.Generator.GetTriggerInterval()
                                                # print("what?")
                        
                                                if ("uS" == time_u):
                                                        t_u = (totalT) * (10 ** -6)
                                                        # print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                elif ("mS" == time_u):
                                                        t_u = (totalT) * (10 ** -3)
                                                        # print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                elif ("S" == time_u):
                                                        t_u = totalT
                                                        # print((float(signal_wait) + float(t_u)) * 2)
                                                        time.sleep((float(signal_wait) + float(t_u)) * 2)
                                                        pass
                                                # print("data scanning ...")
                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                        self.Oscilograph.responseChannel)
                                                # print("kreipimasis", time_unit2)
                                                change, max_y = check_y_scale(data_from_channel2)
                                                # print("max y", max_y, "change", str(change))
                                                if change is True and not self._require_stop:
                                                        while change is True and not self._require_stop:
                                                                self.AMP_OSC_set_parameters(self.Oscilograph.responseChannel,
                                                                                            max_y * 2)
                                                                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                                                                        self.Oscilograph.responseChannel)
                                                                change, max_y = check_y_scale(data_from_channel2)
                                                                if change is False and not self._require_stop:
                                                                        self.AMP_OSC_set_parameters(
                                                                                self.Oscilograph.responseChannel,
                                                                                max_y)
                                                                pass
                                                elif change is False and not self._require_stop:
                                                        self.AMP_OSC_set_parameters(
                                                                self.Oscilograph.responseChannel,
                                                                max_y)
                                                time.sleep(2)
                                                self.OSC_read()
                                                self.progress.emit("measured at " + str(totalT))
                                                totalT = totalT + stepT
                                                print("DEBUG: totalT, stepT", totalT,stepT)
                                                print("DEBUG : ", str(self._require_stop))
                                                if (totalT <= stopT):
                                                        print("DEBUG: totalT, stopT", totalT, stopT)
                                                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                                                self.Oscilograph.unlock_key()
                                                pass
                                        #=============================================================
                                        #=============================================================
                                except Exception as ex:
                                        # print(ex)
                                        self.errors.emit(-1, str(ex) + " " + str(ex.args))
                        else:
                                self.progress.emit("Else fork, stopping ... ")
                                # TODO we need to describe all variants who can occur in if conditions
                                # sys.exit(-1)
                except Exception as ex:
                        exc_type, exc_value, exc_tb = sys.exc_info()
                        traceback.print_exception(exc_type, exc_value, exc_tb)
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
                        # self.progress.emit("Periodas " + str("{0:.8f}".format(t_u)))
                        # time.sleep(wait_pls)
                        pass
                elif ("mS" == unit):
                        t_u = (signal_t / 8) * (10 ** -3)
                        self.Oscilograph.set_closest_time_scale(signal_t / 8, unit)
                        time.sleep(1)
                        self.Oscilograph.set_time_offset(str("{0:.8f}".format(-t_u * 4)))
                        # self.progress.emit("Periodas " + str("{0:.8f}".format(t_u)))
                        pass
                elif ("S" == unit):
                        t_u = signal_t / 8
                        self.Oscilograph.set_closest_time_scale(signal_t / 8, unit)
                        time.sleep(1)
                        self.Oscilograph.set_time_offset(str("{0:.8f}".format(-t_u * 4)))
                        # self.progress.emit("Periodas " + str("{0:.8f}".format(t_u)))
                        pass
                else:
                        self.progress.emit("shit here")
                        pass
                pass
        
        def OSC_read(self):
                self._measurement_parameters["AMPL"]=self._current_ampl
                self._measurement_parameters["OFFS"]=self._current_offs
                self._measurement_parameters["PERIOD"] = self._current_period
                self._measurement_parameters["TIMEU"] = self._current_time_unit
                data_from_channel, time_array, time_unit = self.Oscilograph.get_data_points_from_channel(
                        self.Oscilograph.signalChannel)
                data_from_channel2, time_array2, time_unit2 = self.Oscilograph.get_data_points_from_channel(
                        self.Oscilograph.responseChannel)
                self.results.emit(data_from_channel.tolist(), data_from_channel2.tolist(),
                                  time_array.tolist(), time_unit, self._measurement_parameters)
                pass
        
        def AMP_GEN_set_parameters(self, amplitude, fixed_offset):
                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                time.sleep(0.1)
                self.Generator.SetAmplitude(self.Generator.CH1, amplitude)
                time.sleep(0.1)
                offset = self.GetOffset(amplitude, fixed_offset)
                self.Generator.SetOffset(self.Generator.CH1, offset)
                pass
        
        def OFF_GEN_set_parameters(self, fixed_amplitude, offset):
                self.Generator.EnableOutput(self.Generator.CH1, OFF)
                time.sleep(0.1)
                self.Generator.SetAmplitude(self.Generator.CH1, fixed_amplitude)
                time.sleep(0.1)
                self.Generator.SetOffset(self.Generator.CH1, offset)
                pass
                
        
        def AMP_OSC_set_parameters(self, CH,  amplitude, fixed_offset=0):
                scale = (amplitude + fixed_offset) / 6
                #print("amplitudė " + str(amplitude))
                #print("y offsetas " + str(fixed_offset))
                #print("y skalė " + sc)
                self.Oscilograph.set_closest_voltage_scale(CH, scale)
                time.sleep(1)
                if CH == self.Oscilograph.signalChannel:
                        trigger = amplitude / 4 + fixed_offset
                        tr = str("{0:.2f}".format(trigger))
                        time.sleep(1)
                        self.Oscilograph.set_trigger_edge_level(tr)
                        self.progress.emit(str(tr) + " tr")
                        time.sleep(1)
                        position = -3.0 * scale + (amplitude / 2 - fixed_offset)
                        self.Oscilograph.set_channel_position(CH, str("{0:.3f}".format(position)))
                        #print("signalo skalė: " + str(scale))
                        print("signalo pozicija: " + str("{0:.3f}".format(-3.0 * scale + (amplitude / 2 - fixed_offset))))
                        pass
                if CH == self.Oscilograph.responseChannel:
                        time.sleep(1)
                        self.Oscilograph.set_channel_position(CH, str("{0:.3f}".format(-3.0 * scale)))
                        pass
                # #print(tr, "tr")
                
        
                
                time.sleep(2)  # 100 ms is enough
                pass

        @pyqtSlot()
        def stop(self):
                #print("measurement thread will stop anytime soon")
                self._require_stop = True
                pass
