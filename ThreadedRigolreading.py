from PyQt5.QtCore import *
from PyQt5.QtGui import *

import time

import sys, os
from USBTMC_Devices import *
from GetInfoAboutDevices import *
from ConfigParser import *
import vxi11

class RigolBackGround_scanner(QRunnable):
        '''
        QRunnable based object - do not use for normal long-term tasks!
        '''
        def __init__(self, function, *args, **kwargs):
                super().__init__()
                # init with passed function, args for function, keywords for function
                self.fn = function
                self.args = args
                self.kwargs = kwargs
                self.signals = WorkerSignals()
                pass

        @pyqtSlot()
        def run(self):
                '''
                my code goes here?
                :return:
                '''
                
                time_sleep = float(self.args[1])
                no_more = self.args[2]
                print(time_sleep, "time sleep")
                try:
                        print("try loop")
                        index = 0
                        while index < no_more:
                                data, timeArray, timeUnit = self.fn(str(self.args[0]))
                                # print(result)
                                self.signals.result.emit((data, timeArray, timeUnit))
                                time.sleep(time_sleep)
                                index = index + 1
                        print(index, "Done")
                except Exception as ex:
                        print(ex)
                        self.signals.error.emit(("Error", ex.args))
                finally:
                        self.signals.finished.emit()
                pass



class WorkerSignals(QObject):
        '''
        Just simple class?

        '''
        finished = pyqtSignal()
        error = pyqtSignal(tuple)
        result = pyqtSignal(tuple)
        progress = pyqtSignal(int)
        pass