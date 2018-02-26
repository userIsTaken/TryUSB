# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'experimentPlotWidget.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(431, 509)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.channelOneView = PlotWidget(Form)
        self.channelOneView.setObjectName("channelOneView")
        self.verticalLayout.addWidget(self.channelOneView)
        self.channelTwoView = PlotWidget(Form)
        self.channelTwoView.setObjectName("channelTwoView")
        self.verticalLayout.addWidget(self.channelTwoView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

from pyqtgraph import PlotWidget
