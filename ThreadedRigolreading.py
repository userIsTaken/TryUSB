from PyQt5.QtCore import *
from PyQt5.QtGui import *

import time

import sys, os
from USBTMC_Devices import *
from GetInfoAboutDevices import *
from ConfigParser import *
import vxi11
from MainGUIThread import STOP

class RigolBackGround_scanner(QRunnable):
        def __init__(self, function, *args, **kwargs):
                super().__init__()
                # init with passed function, args for function, keywords for function
                self.fn = function
                self.args = args
                self.kwargs = kwargs
                self.signals = WorkerSignals()
                self.exiting = False
                pass

        def __del__(self):
                self.exiting = True
                pass

        @pyqtSlot()
        def run(self):
                '''
                my code goes here?
                :return:
                '''
                
                time_sleep = float(self.args[1])
                print(time_sleep, "time sleep")
                try:
                        print("try loop")
                        while not self.exiting:
                                print("while loop")
                                # global STOP
                                if STOP:
                                        self.exiting = True
                                        print("global STOP", STOP)
                                data, timeArray, timeUnit = self.fn(str(self.args[0]))
                                # print(result)
                                self.signals.result.emit((data, timeArray, timeUnit))
                                time.sleep(time_sleep)
                except Exception as ex:
                        print(ex)
                        self.signals.error.emit(("Error", ex.args))
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