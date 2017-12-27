from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import os, sys


class LoopWorker(QThread):
        
        results = pyqtSignal(list, list, str)
        errors = pyqtSignal(int, str)
        final = pyqtSignal(int)
        
        def __init__(self, function, *args, **kwargs):
                super(LoopWorker, self).__init__()
                self.fn = function,
                self.args = args
                self.kwargs = kwargs
                pass
        
        @pyqtSlot()
        def run(self):
                pass