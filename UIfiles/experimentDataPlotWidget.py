#!/usr/bin/python3
#-*- utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from UIfiles.experimentPlotWidget import Ui_Form


class experimentPlotWidget(QtWidgets.QWidget):
        def __init__(self, parent=None):
                super(experimentPlotWidget, self).__init__()
                self.ui = Ui_Form()
                self.ui.setupUi(self)