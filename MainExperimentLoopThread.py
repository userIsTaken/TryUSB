from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import os, sys
import time
# from DummyFiles.DummyFunctions import *

class LoopWorker(QThread):
        results = pyqtSignal(list, list, str)
        errors = pyqtSignal(int, str)
        final = pyqtSignal(int)
        
        def __init__(self, function, *args, **kwargs):
                super(LoopWorker, self).__init__()
                # QThread().__init__(self)
                self.fn = function
                self.args = args
                self.kwargs = kwargs
                # self.start() # WHY?????
                print("Init")
                pass
        
        @pyqtSlot()
        def run(self):
                print("Try to run this stuff")
                i = 0
                try:
                        while i <= 100:
                                print("?????", i)
                                result = self.fn(str(self.args[0]))
                                print(result)
                                self.results.emit([5],[5], "BLA!")
                                time.sleep(2)
                                i=i+1
                except Exception as ex:
                        print(ex)
                        pass
                pass
