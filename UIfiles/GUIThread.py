# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUIThread.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainGuiWindow(object):
    def setupUi(self, MainGuiWindow):
        MainGuiWindow.setObjectName("MainGuiWindow")
        MainGuiWindow.resize(900, 800)
        self.centralwidget = QtWidgets.QWidget(MainGuiWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem = QtWidgets.QSpacerItem(278, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.unused_button = QtWidgets.QPushButton(self.centralwidget)
        self.unused_button.setObjectName("unused_button")
        self.horizontalLayout.addWidget(self.unused_button)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.devicesTabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devicesTabWidget.sizePolicy().hasHeightForWidth())
        self.devicesTabWidget.setSizePolicy(sizePolicy)
        self.devicesTabWidget.setMinimumSize(QtCore.QSize(0, 180))
        self.devicesTabWidget.setMaximumSize(QtCore.QSize(16777215, 220))
        self.devicesTabWidget.setObjectName("devicesTabWidget")
        self.usbtmcTab = QtWidgets.QWidget()
        self.usbtmcTab.setObjectName("usbtmcTab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.usbtmcTab)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox_for_generator = QtWidgets.QComboBox(self.usbtmcTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_for_generator.sizePolicy().hasHeightForWidth())
        self.comboBox_for_generator.setSizePolicy(sizePolicy)
        self.comboBox_for_generator.setMinimumSize(QtCore.QSize(220, 0))
        self.comboBox_for_generator.setObjectName("comboBox_for_generator")
        self.gridLayout_2.addWidget(self.comboBox_for_generator, 1, 2, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 5, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.usbtmcTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 6, 1, 1)
        self.label = QtWidgets.QLabel(self.usbtmcTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 6, 1, 1)
        self.comboBox_for_oscillograph = QtWidgets.QComboBox(self.usbtmcTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_for_oscillograph.sizePolicy().hasHeightForWidth())
        self.comboBox_for_oscillograph.setSizePolicy(sizePolicy)
        self.comboBox_for_oscillograph.setMinimumSize(QtCore.QSize(220, 0))
        self.comboBox_for_oscillograph.setObjectName("comboBox_for_oscillograph")
        self.gridLayout_2.addWidget(self.comboBox_for_oscillograph, 2, 2, 1, 2)
        self.findAllUSBTMC_devices_button = QtWidgets.QPushButton(self.usbtmcTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findAllUSBTMC_devices_button.sizePolicy().hasHeightForWidth())
        self.findAllUSBTMC_devices_button.setSizePolicy(sizePolicy)
        self.findAllUSBTMC_devices_button.setObjectName("findAllUSBTMC_devices_button")
        self.gridLayout_2.addWidget(self.findAllUSBTMC_devices_button, 0, 0, 1, 1)
        self.list_of_devices_comboBox = QtWidgets.QComboBox(self.usbtmcTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_of_devices_comboBox.sizePolicy().hasHeightForWidth())
        self.list_of_devices_comboBox.setSizePolicy(sizePolicy)
        self.list_of_devices_comboBox.setMinimumSize(QtCore.QSize(220, 0))
        self.list_of_devices_comboBox.setObjectName("list_of_devices_comboBox")
        self.gridLayout_2.addWidget(self.list_of_devices_comboBox, 0, 2, 1, 1)
        self.custom_info_label = QtWidgets.QLabel(self.usbtmcTab)
        self.custom_info_label.setObjectName("custom_info_label")
        self.gridLayout_2.addWidget(self.custom_info_label, 0, 4, 1, 1)
        self.IDn_generator_label = QtWidgets.QLabel(self.usbtmcTab)
        self.IDn_generator_label.setObjectName("IDn_generator_label")
        self.gridLayout_2.addWidget(self.IDn_generator_label, 1, 4, 1, 2)
        self.selectedIDN_label = QtWidgets.QLabel(self.usbtmcTab)
        self.selectedIDN_label.setObjectName("selectedIDN_label")
        self.gridLayout_2.addWidget(self.selectedIDN_label, 2, 4, 1, 2)
        self.gridLayout_5.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.devicesTabWidget.addTab(self.usbtmcTab, "")
        self.tcpipDevicesTab = QtWidgets.QWidget()
        self.tcpipDevicesTab.setObjectName("tcpipDevicesTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tcpipDevicesTab)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addDeviceEntryTableButton = QtWidgets.QPushButton(self.tcpipDevicesTab)
        self.addDeviceEntryTableButton.setObjectName("addDeviceEntryTableButton")
        self.horizontalLayout_2.addWidget(self.addDeviceEntryTableButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.getIDNfroSelectedIPButton = QtWidgets.QPushButton(self.tcpipDevicesTab)
        self.getIDNfroSelectedIPButton.setObjectName("getIDNfroSelectedIPButton")
        self.horizontalLayout_2.addWidget(self.getIDNfroSelectedIPButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.removeSelectedRowButton = QtWidgets.QPushButton(self.tcpipDevicesTab)
        self.removeSelectedRowButton.setObjectName("removeSelectedRowButton")
        self.horizontalLayout_2.addWidget(self.removeSelectedRowButton)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.tableWithTCPIPDevices = QtWidgets.QTableWidget(self.tcpipDevicesTab)
        self.tableWithTCPIPDevices.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWithTCPIPDevices.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWithTCPIPDevices.setObjectName("tableWithTCPIPDevices")
        self.tableWithTCPIPDevices.setColumnCount(0)
        self.tableWithTCPIPDevices.setRowCount(0)
        self.tableWithTCPIPDevices.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_4.addWidget(self.tableWithTCPIPDevices, 1, 0, 1, 1)
        self.devicesTabWidget.addTab(self.tcpipDevicesTab, "")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setObjectName("tabWidget")
        self.oscligraph_tab = QtWidgets.QWidget()
        self.oscligraph_tab.setObjectName("oscligraph_tab")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.oscligraph_tab)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.connectToOscilograph_button = QtWidgets.QPushButton(self.oscligraph_tab)
        self.connectToOscilograph_button.setObjectName("connectToOscilograph_button")
        self.gridLayout_10.addWidget(self.connectToOscilograph_button, 0, 0, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.idn_label_oscilograph = QtWidgets.QLabel(self.oscligraph_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.idn_label_oscilograph.sizePolicy().hasHeightForWidth())
        self.idn_label_oscilograph.setSizePolicy(sizePolicy)
        self.idn_label_oscilograph.setMinimumSize(QtCore.QSize(220, 0))
        self.idn_label_oscilograph.setObjectName("idn_label_oscilograph")
        self.gridLayout_8.addWidget(self.idn_label_oscilograph, 0, 0, 1, 3)
        self.getVoltsFromCH1_button = QtWidgets.QPushButton(self.oscligraph_tab)
        self.getVoltsFromCH1_button.setObjectName("getVoltsFromCH1_button")
        self.gridLayout_8.addWidget(self.getVoltsFromCH1_button, 1, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem6, 1, 1, 1, 1)
        self.getVoltasFromCH2_button = QtWidgets.QPushButton(self.oscligraph_tab)
        self.getVoltasFromCH2_button.setObjectName("getVoltasFromCH2_button")
        self.gridLayout_8.addWidget(self.getVoltasFromCH2_button, 1, 2, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_8, 1, 0, 1, 1)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.getDatafromBothChannels_button = QtWidgets.QPushButton(self.oscligraph_tab)
        self.getDatafromBothChannels_button.setObjectName("getDatafromBothChannels_button")
        self.gridLayout_9.addWidget(self.getDatafromBothChannels_button, 0, 0, 1, 2)
        self.useRegularUpdateBox = QtWidgets.QCheckBox(self.oscligraph_tab)
        self.useRegularUpdateBox.setObjectName("useRegularUpdateBox")
        self.gridLayout_9.addWidget(self.useRegularUpdateBox, 1, 0, 1, 1)
        self.secondsToWait = QtWidgets.QDoubleSpinBox(self.oscligraph_tab)
        self.secondsToWait.setProperty("value", 3.0)
        self.secondsToWait.setObjectName("secondsToWait")
        self.gridLayout_9.addWidget(self.secondsToWait, 1, 1, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_9, 2, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 70, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem7, 3, 0, 1, 1)
        self.plainConfigOscilograph = QtWidgets.QPlainTextEdit(self.oscligraph_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainConfigOscilograph.sizePolicy().hasHeightForWidth())
        self.plainConfigOscilograph.setSizePolicy(sizePolicy)
        self.plainConfigOscilograph.setObjectName("plainConfigOscilograph")
        self.gridLayout_10.addWidget(self.plainConfigOscilograph, 4, 0, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem8, 0, 1, 1, 1)
        self.dataViewWidget = PlotWidget(self.oscligraph_tab)
        self.dataViewWidget.setMinimumSize(QtCore.QSize(450, 320))
        self.dataViewWidget.setObjectName("dataViewWidget")
        self.gridLayout_11.addWidget(self.dataViewWidget, 0, 2, 1, 1)
        self.tabWidget.addTab(self.oscligraph_tab, "")
        self.generator_tab = QtWidgets.QWidget()
        self.generator_tab.setObjectName("generator_tab")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.generator_tab)
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.connectToGeneratorButton = QtWidgets.QPushButton(self.generator_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectToGeneratorButton.sizePolicy().hasHeightForWidth())
        self.connectToGeneratorButton.setSizePolicy(sizePolicy)
        self.connectToGeneratorButton.setObjectName("connectToGeneratorButton")
        self.gridLayout_16.addWidget(self.connectToGeneratorButton, 0, 0, 1, 1)
        self.runInitiallConfiguration_button = QtWidgets.QPushButton(self.generator_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runInitiallConfiguration_button.sizePolicy().hasHeightForWidth())
        self.runInitiallConfiguration_button.setSizePolicy(sizePolicy)
        self.runInitiallConfiguration_button.setObjectName("runInitiallConfiguration_button")
        self.gridLayout_16.addWidget(self.runInitiallConfiguration_button, 0, 1, 1, 1)
        self.connection_status_label = QtWidgets.QLabel(self.generator_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connection_status_label.sizePolicy().hasHeightForWidth())
        self.connection_status_label.setSizePolicy(sizePolicy)
        self.connection_status_label.setObjectName("connection_status_label")
        self.gridLayout_16.addWidget(self.connection_status_label, 1, 0, 1, 2)
        self.gridLayout_18.addLayout(self.gridLayout_16, 0, 0, 1, 1)
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.setSignalAmplitudeButton = QtWidgets.QPushButton(self.generator_tab)
        self.setSignalAmplitudeButton.setMaximumSize(QtCore.QSize(230, 16777215))
        self.setSignalAmplitudeButton.setObjectName("setSignalAmplitudeButton")
        self.gridLayout_15.addWidget(self.setSignalAmplitudeButton, 0, 0, 1, 1)
        self.voltageAmplitudeBox = QtWidgets.QDoubleSpinBox(self.generator_tab)
        self.voltageAmplitudeBox.setMinimumSize(QtCore.QSize(120, 0))
        self.voltageAmplitudeBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.voltageAmplitudeBox.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        self.voltageAmplitudeBox.setDecimals(3)
        self.voltageAmplitudeBox.setObjectName("voltageAmplitudeBox")
        self.gridLayout_15.addWidget(self.voltageAmplitudeBox, 0, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_15.addItem(spacerItem9, 0, 2, 1, 1)
        self.setOffsetButton = QtWidgets.QPushButton(self.generator_tab)
        self.setOffsetButton.setMinimumSize(QtCore.QSize(230, 0))
        self.setOffsetButton.setMaximumSize(QtCore.QSize(230, 16777215))
        self.setOffsetButton.setObjectName("setOffsetButton")
        self.gridLayout_15.addWidget(self.setOffsetButton, 1, 0, 1, 1)
        self.voltageOffsetBox = QtWidgets.QDoubleSpinBox(self.generator_tab)
        self.voltageOffsetBox.setMinimumSize(QtCore.QSize(120, 0))
        self.voltageOffsetBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.voltageOffsetBox.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        self.voltageOffsetBox.setDecimals(3)
        self.voltageOffsetBox.setObjectName("voltageOffsetBox")
        self.gridLayout_15.addWidget(self.voltageOffsetBox, 1, 1, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_15.addItem(spacerItem10, 1, 2, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_15, 1, 0, 1, 1)
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.setBurstNCyclesButton = QtWidgets.QPushButton(self.generator_tab)
        self.setBurstNCyclesButton.setMinimumSize(QtCore.QSize(230, 0))
        self.setBurstNCyclesButton.setMaximumSize(QtCore.QSize(230, 16777215))
        self.setBurstNCyclesButton.setObjectName("setBurstNCyclesButton")
        self.gridLayout_17.addWidget(self.setBurstNCyclesButton, 0, 0, 1, 2)
        self.InputOutputCH1Button = QtWidgets.QPushButton(self.generator_tab)
        self.InputOutputCH1Button.setCheckable(True)
        self.InputOutputCH1Button.setObjectName("InputOutputCH1Button")
        self.gridLayout_17.addWidget(self.InputOutputCH1Button, 1, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_17.addItem(spacerItem11, 1, 1, 1, 2)
        self.InputOutputCH2Button = QtWidgets.QPushButton(self.generator_tab)
        self.InputOutputCH2Button.setCheckable(True)
        self.InputOutputCH2Button.setObjectName("InputOutputCH2Button")
        self.gridLayout_17.addWidget(self.InputOutputCH2Button, 1, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.generator_tab)
        self.label_8.setObjectName("label_8")
        self.gridLayout_17.addWidget(self.label_8, 2, 0, 1, 4)
        self.nCyclesBox = QtWidgets.QDoubleSpinBox(self.generator_tab)
        self.nCyclesBox.setMinimumSize(QtCore.QSize(120, 0))
        self.nCyclesBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.nCyclesBox.setObjectName("nCyclesBox")
        self.gridLayout_17.addWidget(self.nCyclesBox, 0, 2, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_17, 4, 0, 1, 1)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.setPeriodButton = QtWidgets.QPushButton(self.generator_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setPeriodButton.sizePolicy().hasHeightForWidth())
        self.setPeriodButton.setSizePolicy(sizePolicy)
        self.setPeriodButton.setMinimumSize(QtCore.QSize(230, 0))
        self.setPeriodButton.setMaximumSize(QtCore.QSize(230, 16777215))
        self.setPeriodButton.setObjectName("setPeriodButton")
        self.gridLayout_13.addWidget(self.setPeriodButton, 0, 0, 1, 1)
        self.periodBox = QtWidgets.QDoubleSpinBox(self.generator_tab)
        self.periodBox.setMinimumSize(QtCore.QSize(120, 0))
        self.periodBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.periodBox.setDecimals(0)
        self.periodBox.setMaximum(100000.0)
        self.periodBox.setObjectName("periodBox")
        self.gridLayout_13.addWidget(self.periodBox, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.generator_tab)
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
        self.gridLayout_13.addWidget(self.groupBox, 0, 2, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_13, 2, 0, 1, 1)
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.setTriggerIntervalButton = QtWidgets.QPushButton(self.generator_tab)
        self.setTriggerIntervalButton.setMaximumSize(QtCore.QSize(230, 16777215))
        self.setTriggerIntervalButton.setObjectName("setTriggerIntervalButton")
        self.gridLayout_14.addWidget(self.setTriggerIntervalButton, 0, 0, 1, 1)
        self.triggerIntervalBox = QtWidgets.QDoubleSpinBox(self.generator_tab)
        self.triggerIntervalBox.setMinimumSize(QtCore.QSize(120, 0))
        self.triggerIntervalBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.triggerIntervalBox.setDecimals(0)
        self.triggerIntervalBox.setMaximum(1000000.0)
        self.triggerIntervalBox.setObjectName("triggerIntervalBox")
        self.gridLayout_14.addWidget(self.triggerIntervalBox, 0, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.generator_tab)
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
        self.gridLayout_14.addWidget(self.groupBox_2, 0, 2, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_14, 3, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.sendCustomCmd_gen_button = QtWidgets.QPushButton(self.generator_tab)
        self.sendCustomCmd_gen_button.setMaximumSize(QtCore.QSize(120, 16777215))
        self.sendCustomCmd_gen_button.setObjectName("sendCustomCmd_gen_button")
        self.gridLayout_6.addWidget(self.sendCustomCmd_gen_button, 0, 0, 1, 1)
        self.cmd_custom_for_generator = QtWidgets.QComboBox(self.generator_tab)
        self.cmd_custom_for_generator.setMinimumSize(QtCore.QSize(300, 0))
        self.cmd_custom_for_generator.setEditable(True)
        self.cmd_custom_for_generator.setMaxVisibleItems(25)
        self.cmd_custom_for_generator.setObjectName("cmd_custom_for_generator")
        self.gridLayout_6.addWidget(self.cmd_custom_for_generator, 0, 1, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_6, 5, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_18.addItem(spacerItem12, 6, 0, 1, 1)
        self.initialConfigurationForGenerator = QtWidgets.QPlainTextEdit(self.generator_tab)
        self.initialConfigurationForGenerator.setObjectName("initialConfigurationForGenerator")
        self.gridLayout_18.addWidget(self.initialConfigurationForGenerator, 0, 1, 7, 1)
        self.tabWidget.addTab(self.generator_tab, "")
        self.expSessionTab = QtWidgets.QWidget()
        self.expSessionTab.setObjectName("expSessionTab")
        self.tabWidget.addTab(self.expSessionTab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.clearErrorTextButton = QtWidgets.QPushButton(self.tab)
        self.clearErrorTextButton.setObjectName("clearErrorTextButton")
        self.gridLayout.addWidget(self.clearErrorTextButton, 0, 0, 1, 1)
        self.advancedTextEditForErrors = QtWidgets.QTextEdit(self.tab)
        self.advancedTextEditForErrors.setObjectName("advancedTextEditForErrors")
        self.gridLayout.addWidget(self.advancedTextEditForErrors, 1, 0, 1, 2)
        spacerItem13 = QtWidgets.QSpacerItem(367, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem13, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        MainGuiWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainGuiWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 30))
        self.menubar.setObjectName("menubar")
        self.menuFailas = QtWidgets.QMenu(self.menubar)
        self.menuFailas.setObjectName("menuFailas")
        MainGuiWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainGuiWindow)
        self.statusbar.setObjectName("statusbar")
        MainGuiWindow.setStatusBar(self.statusbar)
        self.actionU_daryti = QtWidgets.QAction(MainGuiWindow)
        self.actionU_daryti.setObjectName("actionU_daryti")
        self.actionI_saugoti_DAT = QtWidgets.QAction(MainGuiWindow)
        self.actionI_saugoti_DAT.setObjectName("actionI_saugoti_DAT")
        self.actionI_saugoti_TXT = QtWidgets.QAction(MainGuiWindow)
        self.actionI_saugoti_TXT.setObjectName("actionI_saugoti_TXT")
        self.actionI_saugoti_QTI_projekt = QtWidgets.QAction(MainGuiWindow)
        self.actionI_saugoti_QTI_projekt.setObjectName("actionI_saugoti_QTI_projekt")
        self.menuFailas.addAction(self.actionU_daryti)
        self.menuFailas.addAction(self.actionI_saugoti_DAT)
        self.menuFailas.addAction(self.actionI_saugoti_TXT)
        self.menuFailas.addAction(self.actionI_saugoti_QTI_projekt)
        self.menubar.addAction(self.menuFailas.menuAction())

        self.retranslateUi(MainGuiWindow)
        self.devicesTabWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainGuiWindow)

    def retranslateUi(self, MainGuiWindow):
        _translate = QtCore.QCoreApplication.translate
        MainGuiWindow.setWindowTitle(_translate("MainGuiWindow", "GenOsci"))
        self.closeButton.setText(_translate("MainGuiWindow", "Išeiti iš programos"))
        self.unused_button.setText(_translate("MainGuiWindow", "Neveikiantis mygis"))
        self.label_2.setText(_translate("MainGuiWindow", "Generatorius"))
        self.label.setText(_translate("MainGuiWindow", "Oscilografas:"))
        self.findAllUSBTMC_devices_button.setText(_translate("MainGuiWindow", "Prietaisai"))
        self.custom_info_label.setText(_translate("MainGuiWindow", "/DEV"))
        self.IDn_generator_label.setText(_translate("MainGuiWindow", "*IDN?"))
        self.selectedIDN_label.setText(_translate("MainGuiWindow", "*IDN?"))
        self.devicesTabWidget.setTabText(self.devicesTabWidget.indexOf(self.usbtmcTab), _translate("MainGuiWindow", "USBTMC prietaisai"))
        self.addDeviceEntryTableButton.setText(_translate("MainGuiWindow", "Pridėti naują eilutę"))
        self.getIDNfroSelectedIPButton.setText(_translate("MainGuiWindow", "*IDN?"))
        self.removeSelectedRowButton.setText(_translate("MainGuiWindow", "Pašalinti įrašą"))
        self.devicesTabWidget.setTabText(self.devicesTabWidget.indexOf(self.tcpipDevicesTab), _translate("MainGuiWindow", "Tinklo (TCP/IP) prietaisai"))
        self.connectToOscilograph_button.setText(_translate("MainGuiWindow", "Prisijungti prie oscilografo"))
        self.idn_label_oscilograph.setText(_translate("MainGuiWindow", "IDN, jei sėkmingai"))
        self.getVoltsFromCH1_button.setText(_translate("MainGuiWindow", "CH1 duomenys"))
        self.getVoltasFromCH2_button.setText(_translate("MainGuiWindow", "CH2 duomenys"))
        self.getDatafromBothChannels_button.setText(_translate("MainGuiWindow", "Nuskaityti abu kanalus"))
        self.useRegularUpdateBox.setText(_translate("MainGuiWindow", "Atnaujinti kas [s]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.oscligraph_tab), _translate("MainGuiWindow", "Oscilografas"))
        self.connectToGeneratorButton.setText(_translate("MainGuiWindow", "Prisijunti prie generatoriaus"))
        self.runInitiallConfiguration_button.setText(_translate("MainGuiWindow", "Pirminė konfigūracija"))
        self.connection_status_label.setText(_translate("MainGuiWindow", "IDN, jei pavyko prisijunti"))
        self.setSignalAmplitudeButton.setText(_translate("MainGuiWindow", "Signalo amplitudė, V"))
        self.setOffsetButton.setText(_translate("MainGuiWindow", "Signalo nuokrypis (offset), V"))
        self.setBurstNCyclesButton.setText(_translate("MainGuiWindow", "Ciklų kiekis (BURST NCYCLES)"))
        self.InputOutputCH1Button.setText(_translate("MainGuiWindow", "CH1"))
        self.InputOutputCH2Button.setText(_translate("MainGuiWindow", "CH2"))
        self.label_8.setText(_translate("MainGuiWindow", "Nustatytas dažnis, Hz|kHz|MHz = "))
        self.setPeriodButton.setText(_translate("MainGuiWindow", "Periodas, μs|ms|s"))
        self.groupBox.setTitle(_translate("MainGuiWindow", "Laiko vienetai periodui"))
        self.periodRadioButton_uS.setText(_translate("MainGuiWindow", "μS"))
        self.periodRadioButton_mS.setText(_translate("MainGuiWindow", "mS"))
        self.periodradioButton_S.setText(_translate("MainGuiWindow", "S"))
        self.setTriggerIntervalButton.setText(_translate("MainGuiWindow", "Trigerio intervalas, μs|ms|s"))
        self.groupBox_2.setTitle(_translate("MainGuiWindow", "Laiko vienetai trigeriui"))
        self.triggerInterval_uS.setText(_translate("MainGuiWindow", "μS"))
        self.triggerInterval_mS.setText(_translate("MainGuiWindow", "mS"))
        self.triggerInterval_S.setText(_translate("MainGuiWindow", "S"))
        self.sendCustomCmd_gen_button.setText(_translate("MainGuiWindow", "Siųsti CMD"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generator_tab), _translate("MainGuiWindow", "Generatorius"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.expSessionTab), _translate("MainGuiWindow", "Eksperimentas"))
        self.clearErrorTextButton.setText(_translate("MainGuiWindow", "Išvalyti klaidų pranešimus"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainGuiWindow", "Klaidų/informacijos pranešimai"))
        self.menuFailas.setTitle(_translate("MainGuiWindow", "Failas"))
        self.actionU_daryti.setText(_translate("MainGuiWindow", "Uždaryti"))
        self.actionI_saugoti_DAT.setText(_translate("MainGuiWindow", "Išsaugoti į DAT"))
        self.actionI_saugoti_TXT.setText(_translate("MainGuiWindow", "Išsaugoti į TXT"))
        self.actionI_saugoti_QTI_projekt.setText(_translate("MainGuiWindow", "Išsaugoti į QTI projektą"))

from pyqtgraph import PlotWidget
