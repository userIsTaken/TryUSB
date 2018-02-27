# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GeneraratorChannelConfig.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GeneratorChannelConfigForm(object):
    def setupUi(self, GeneratorChannelConfigForm):
        GeneratorChannelConfigForm.setObjectName("GeneratorChannelConfigForm")
        GeneratorChannelConfigForm.resize(532, 270)
        GeneratorChannelConfigForm.setMinimumSize(QtCore.QSize(500, 250))
        GeneratorChannelConfigForm.setMaximumSize(QtCore.QSize(550, 270))
        self.gridLayout = QtWidgets.QGridLayout(GeneratorChannelConfigForm)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.setSignalAmplitudeButton = QtWidgets.QPushButton(GeneratorChannelConfigForm)
        self.setSignalAmplitudeButton.setMinimumSize(QtCore.QSize(200, 0))
        self.setSignalAmplitudeButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.setSignalAmplitudeButton.setObjectName("setSignalAmplitudeButton")
        self.horizontalLayout_3.addWidget(self.setSignalAmplitudeButton)
        self.voltageAmplitudeBox = QtWidgets.QDoubleSpinBox(GeneratorChannelConfigForm)
        self.voltageAmplitudeBox.setMinimumSize(QtCore.QSize(120, 0))
        self.voltageAmplitudeBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.voltageAmplitudeBox.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        self.voltageAmplitudeBox.setDecimals(3)
        self.voltageAmplitudeBox.setMaximum(10.0)
        self.voltageAmplitudeBox.setObjectName("voltageAmplitudeBox")
        self.horizontalLayout_3.addWidget(self.voltageAmplitudeBox)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(177, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.setOffsetButton = QtWidgets.QPushButton(GeneratorChannelConfigForm)
        self.setOffsetButton.setMinimumSize(QtCore.QSize(200, 0))
        self.setOffsetButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.setOffsetButton.setObjectName("setOffsetButton")
        self.horizontalLayout_4.addWidget(self.setOffsetButton)
        self.voltageOffsetBox = QtWidgets.QDoubleSpinBox(GeneratorChannelConfigForm)
        self.voltageOffsetBox.setMinimumSize(QtCore.QSize(120, 0))
        self.voltageOffsetBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.voltageOffsetBox.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        self.voltageOffsetBox.setDecimals(3)
        self.voltageOffsetBox.setMinimum(-10.0)
        self.voltageOffsetBox.setMaximum(10.0)
        self.voltageOffsetBox.setObjectName("voltageOffsetBox")
        self.horizontalLayout_4.addWidget(self.voltageOffsetBox)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(177, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.setTriggerIntervalButton = QtWidgets.QPushButton(GeneratorChannelConfigForm)
        self.setTriggerIntervalButton.setMinimumSize(QtCore.QSize(200, 0))
        self.setTriggerIntervalButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.setTriggerIntervalButton.setObjectName("setTriggerIntervalButton")
        self.horizontalLayout.addWidget(self.setTriggerIntervalButton)
        self.triggerIntervalBox = QtWidgets.QDoubleSpinBox(GeneratorChannelConfigForm)
        self.triggerIntervalBox.setMinimumSize(QtCore.QSize(120, 0))
        self.triggerIntervalBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.triggerIntervalBox.setDecimals(0)
        self.triggerIntervalBox.setMaximum(1000000.0)
        self.triggerIntervalBox.setObjectName("triggerIntervalBox")
        self.horizontalLayout.addWidget(self.triggerIntervalBox)
        self.groupBox_2 = QtWidgets.QGroupBox(GeneratorChannelConfigForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.triggerInterval_uS = QtWidgets.QRadioButton(self.groupBox_2)
        self.triggerInterval_uS.setObjectName("triggerInterval_uS")
        self.gridLayout_12.addWidget(self.triggerInterval_uS, 0, 0, 1, 1)
        self.triggerInterval_mS = QtWidgets.QRadioButton(self.groupBox_2)
        self.triggerInterval_mS.setChecked(True)
        self.triggerInterval_mS.setObjectName("triggerInterval_mS")
        self.gridLayout_12.addWidget(self.triggerInterval_mS, 0, 1, 1, 1)
        self.triggerInterval_S = QtWidgets.QRadioButton(self.groupBox_2)
        self.triggerInterval_S.setObjectName("triggerInterval_S")
        self.gridLayout_12.addWidget(self.triggerInterval_S, 0, 2, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.setPeriodButton = QtWidgets.QPushButton(GeneratorChannelConfigForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setPeriodButton.sizePolicy().hasHeightForWidth())
        self.setPeriodButton.setSizePolicy(sizePolicy)
        self.setPeriodButton.setMinimumSize(QtCore.QSize(200, 0))
        self.setPeriodButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.setPeriodButton.setObjectName("setPeriodButton")
        self.horizontalLayout_2.addWidget(self.setPeriodButton)
        self.periodBox = QtWidgets.QDoubleSpinBox(GeneratorChannelConfigForm)
        self.periodBox.setMinimumSize(QtCore.QSize(120, 0))
        self.periodBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.periodBox.setDecimals(0)
        self.periodBox.setMaximum(100000.0)
        self.periodBox.setObjectName("periodBox")
        self.horizontalLayout_2.addWidget(self.periodBox)
        self.groupBox = QtWidgets.QGroupBox(GeneratorChannelConfigForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.periodRadioButton_uS = QtWidgets.QRadioButton(self.groupBox)
        self.periodRadioButton_uS.setObjectName("periodRadioButton_uS")
        self.gridLayout_7.addWidget(self.periodRadioButton_uS, 0, 0, 1, 1)
        self.periodRadioButton_mS = QtWidgets.QRadioButton(self.groupBox)
        self.periodRadioButton_mS.setChecked(True)
        self.periodRadioButton_mS.setObjectName("periodRadioButton_mS")
        self.gridLayout_7.addWidget(self.periodRadioButton_mS, 0, 1, 1, 1)
        self.periodradioButton_S = QtWidgets.QRadioButton(self.groupBox)
        self.periodradioButton_S.setObjectName("periodradioButton_S")
        self.gridLayout_7.addWidget(self.periodradioButton_S, 0, 2, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.setBurstNCyclesButton = QtWidgets.QPushButton(GeneratorChannelConfigForm)
        self.setBurstNCyclesButton.setMinimumSize(QtCore.QSize(200, 0))
        self.setBurstNCyclesButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.setBurstNCyclesButton.setObjectName("setBurstNCyclesButton")
        self.horizontalLayout_5.addWidget(self.setBurstNCyclesButton)
        self.nCyclesBox = QtWidgets.QDoubleSpinBox(GeneratorChannelConfigForm)
        self.nCyclesBox.setMinimumSize(QtCore.QSize(120, 0))
        self.nCyclesBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.nCyclesBox.setDecimals(0)
        self.nCyclesBox.setMaximum(10000000.0)
        self.nCyclesBox.setObjectName("nCyclesBox")
        self.horizontalLayout_5.addWidget(self.nCyclesBox)
        self.gridLayout.addLayout(self.horizontalLayout_5, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(177, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)

        self.retranslateUi(GeneratorChannelConfigForm)
        QtCore.QMetaObject.connectSlotsByName(GeneratorChannelConfigForm)

    def retranslateUi(self, GeneratorChannelConfigForm):
        _translate = QtCore.QCoreApplication.translate
        GeneratorChannelConfigForm.setWindowTitle(_translate("GeneratorChannelConfigForm", "Form"))
        self.setSignalAmplitudeButton.setText(_translate("GeneratorChannelConfigForm", "Signalo amplitudė, V"))
        self.setOffsetButton.setText(_translate("GeneratorChannelConfigForm", "Signalo nuokrypis, V"))
        self.setTriggerIntervalButton.setText(_translate("GeneratorChannelConfigForm", "Trigerio intervalas"))
        self.groupBox_2.setTitle(_translate("GeneratorChannelConfigForm", "Laiko vienetai trigeriui"))
        self.triggerInterval_uS.setText(_translate("GeneratorChannelConfigForm", "μS"))
        self.triggerInterval_mS.setText(_translate("GeneratorChannelConfigForm", "mS"))
        self.triggerInterval_S.setText(_translate("GeneratorChannelConfigForm", "S"))
        self.setPeriodButton.setText(_translate("GeneratorChannelConfigForm", "Periodas"))
        self.groupBox.setTitle(_translate("GeneratorChannelConfigForm", "Laiko vienetai periodui"))
        self.periodRadioButton_uS.setText(_translate("GeneratorChannelConfigForm", "μS"))
        self.periodRadioButton_mS.setText(_translate("GeneratorChannelConfigForm", "mS"))
        self.periodradioButton_S.setText(_translate("GeneratorChannelConfigForm", "S"))
        self.setBurstNCyclesButton.setText(_translate("GeneratorChannelConfigForm", "Ciklų kiekis"))

