from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import os, sys
# from DummyFiles.DummyFunctions import *

class LoopWorker(QThread):
        results = pyqtSignal(list, list, str)
        errors = pyqtSignal(int, str)
        final = pyqtSignal(int)
        
        def __init__(self, function, *args, **kwargs):
                super(LoopWorker, self).__init__()
                self.fn = function,
                self.args = args
                self.kwargs = kwargs
                print("Init")
                pass
        
        @pyqtSlot()
        def work(self):
                print("Try to run this stuff")
                try:
                        result = self.fn(str(self.args[0]))
                        print(result)
                        self.results.emit([5],[5], "BLA!")
                except Exception as ex:
                        print(ex)
                        pass
                pass
