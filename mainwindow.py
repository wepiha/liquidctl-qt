# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wepiha/Documents/nzxqt/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 830)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabCooling = QtWidgets.QWidget()
        self.tabCooling.setObjectName("tabCooling")
        self.widget = QtWidgets.QWidget(self.tabCooling)
        self.widget.setGeometry(QtCore.QRect(153, 13, 466, 241))
        self.widget.setStyleSheet("background-color: black")
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.tabCooling)
        self.widget_2.setGeometry(QtCore.QRect(155, 279, 463, 247))
        self.widget_2.setStyleSheet("background-color: black")
        self.widget_2.setObjectName("widget_2")
        self.tabWidget.addTab(self.tabCooling, "")
        self.tabLighting = QtWidgets.QWidget()
        self.tabLighting.setObjectName("tabLighting")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tabLighting)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtChart.QChartView(self.tabLighting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(200, 180))
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.labelLogo = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.labelLogo.setFont(font)
        self.labelLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLogo.setObjectName("labelLogo")
        self.gridLayout_3.addWidget(self.labelLogo, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 2, 1, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem4 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_6.addItem(spacerItem4)
        self.labelPresetRevert = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(True)
        self.labelPresetRevert.setFont(font)
        self.labelPresetRevert.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.labelPresetRevert.setIndent(4)
        self.labelPresetRevert.setObjectName("labelPresetRevert")
        self.verticalLayout_6.addWidget(self.labelPresetRevert)
        self.gridLayout_3.addLayout(self.verticalLayout_6, 2, 2, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem5 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_7.addItem(spacerItem5)
        self.labelPresetRevert_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(True)
        self.labelPresetRevert_2.setFont(font)
        self.labelPresetRevert_2.setText("")
        self.labelPresetRevert_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.labelPresetRevert_2.setIndent(4)
        self.labelPresetRevert_2.setObjectName("labelPresetRevert_2")
        self.verticalLayout_7.addWidget(self.labelPresetRevert_2)
        self.gridLayout_3.addLayout(self.verticalLayout_7, 2, 0, 1, 1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.labelPresetRevert_3 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(True)
        self.labelPresetRevert_3.setFont(font)
        self.labelPresetRevert_3.setText("")
        self.labelPresetRevert_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelPresetRevert_3.setIndent(4)
        self.labelPresetRevert_3.setObjectName("labelPresetRevert_3")
        self.verticalLayout_8.addWidget(self.labelPresetRevert_3)
        spacerItem6 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_8.addItem(spacerItem6)
        self.gridLayout_3.addLayout(self.verticalLayout_8, 0, 0, 1, 1)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.labelPresetRevert_4 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(True)
        self.labelPresetRevert_4.setFont(font)
        self.labelPresetRevert_4.setText("")
        self.labelPresetRevert_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.labelPresetRevert_4.setIndent(4)
        self.labelPresetRevert_4.setObjectName("labelPresetRevert_4")
        self.verticalLayout_9.addWidget(self.labelPresetRevert_4)
        spacerItem7 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_9.addItem(spacerItem7)
        self.gridLayout_3.addLayout(self.verticalLayout_9, 0, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem8)
        self.labelEffectSelection = QtWidgets.QLabel(self.tabLighting)
        self.labelEffectSelection.setMinimumSize(QtCore.QSize(120, 0))
        self.labelEffectSelection.setObjectName("labelEffectSelection")
        self.verticalLayout_4.addWidget(self.labelEffectSelection)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButtonPresetLogo = QtWidgets.QRadioButton(self.tabLighting)
        self.radioButtonPresetLogo.setObjectName("radioButtonPresetLogo")
        self.verticalLayout_3.addWidget(self.radioButtonPresetLogo)
        self.radioButtonPresetRing = QtWidgets.QRadioButton(self.tabLighting)
        self.radioButtonPresetRing.setObjectName("radioButtonPresetRing")
        self.verticalLayout_3.addWidget(self.radioButtonPresetRing)
        self.radioButtonPresetBoth = QtWidgets.QRadioButton(self.tabLighting)
        self.radioButtonPresetBoth.setChecked(True)
        self.radioButtonPresetBoth.setObjectName("radioButtonPresetBoth")
        self.verticalLayout_3.addWidget(self.radioButtonPresetBoth)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelLogoMode = QtWidgets.QLabel(self.tabLighting)
        self.labelLogoMode.setMinimumSize(QtCore.QSize(300, 0))
        self.labelLogoMode.setObjectName("labelLogoMode")
        self.verticalLayout.addWidget(self.labelLogoMode)
        self.labelRingMode = QtWidgets.QLabel(self.tabLighting)
        self.labelRingMode.setMinimumSize(QtCore.QSize(120, 0))
        self.labelRingMode.setObjectName("labelRingMode")
        self.verticalLayout.addWidget(self.labelRingMode)
        self.labelBothMode = QtWidgets.QLabel(self.tabLighting)
        self.labelBothMode.setMinimumSize(QtCore.QSize(120, 0))
        self.labelBothMode.setObjectName("labelBothMode")
        self.verticalLayout.addWidget(self.labelBothMode)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem9)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        spacerItem10 = QtWidgets.QSpacerItem(147, 179, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tabLighting)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_2_1 = QtWidgets.QWidget()
        self.tab_2_1.setObjectName("tab_2_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mdiArea = QtWidgets.QMdiArea(self.tab_2_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy)
        self.mdiArea.setMinimumSize(QtCore.QSize(0, 400))
        self.mdiArea.setMaximumSize(QtCore.QSize(564, 400))
        self.mdiArea.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.mdiArea.setObjectName("mdiArea")
        self.gridLayout_2.addWidget(self.mdiArea, 0, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem11, 1, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.line_2 = QtWidgets.QFrame(self.tab_2_1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.label_2 = QtWidgets.QLabel(self.tab_2_1)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.comboBoxPresetModes = QtWidgets.QComboBox(self.tab_2_1)
        self.comboBoxPresetModes.setObjectName("comboBoxPresetModes")
        self.verticalLayout_2.addWidget(self.comboBoxPresetModes)
        self.labelPresetAniSpeedLabel = QtWidgets.QLabel(self.tab_2_1)
        self.labelPresetAniSpeedLabel.setMinimumSize(QtCore.QSize(180, 0))
        self.labelPresetAniSpeedLabel.setObjectName("labelPresetAniSpeedLabel")
        self.verticalLayout_2.addWidget(self.labelPresetAniSpeedLabel)
        self.horizontalSliderASpeed = QtWidgets.QSlider(self.tab_2_1)
        self.horizontalSliderASpeed.setMinimum(0)
        self.horizontalSliderASpeed.setMaximum(4)
        self.horizontalSliderASpeed.setPageStep(1)
        self.horizontalSliderASpeed.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderASpeed.setObjectName("horizontalSliderASpeed")
        self.verticalLayout_2.addWidget(self.horizontalSliderASpeed)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem12)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_2_1, "")
        self.tab_2_2 = QtWidgets.QWidget()
        self.tab_2_2.setObjectName("tab_2_2")
        self.tabWidget_2.addTab(self.tab_2_2, "")
        self.gridLayout_5.addWidget(self.tabWidget_2, 1, 0, 1, 1)
        self.pushButtonSave = QtWidgets.QPushButton(self.tabLighting)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.gridLayout_5.addWidget(self.pushButtonSave, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tabLighting, "")
        self.tabOverclock = QtWidgets.QWidget()
        self.tabOverclock.setObjectName("tabOverclock")
        self.tabWidget.addTab(self.tabOverclock, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelDevDeviceName = QtWidgets.QLabel(self.centralwidget)
        self.labelDevDeviceName.setObjectName("labelDevDeviceName")
        self.horizontalLayout_4.addWidget(self.labelDevDeviceName)
        self.labelDevSerialNo = QtWidgets.QLabel(self.centralwidget)
        self.labelDevSerialNo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelDevSerialNo.setObjectName("labelDevSerialNo")
        self.horizontalLayout_4.addWidget(self.labelDevSerialNo)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDevice = QtWidgets.QMenu(self.menubar)
        self.menuDevice.setObjectName("menuDevice")
        self.menu_Select_Device = QtWidgets.QMenu(self.menuDevice)
        self.menu_Select_Device.setObjectName("menu_Select_Device")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionReload = QtWidgets.QAction(MainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actiondummy = QtWidgets.QAction(MainWindow)
        self.actiondummy.setObjectName("actiondummy")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionReset)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menu_Select_Device.addAction(self.actiondummy)
        self.menuDevice.addAction(self.menu_Select_Device.menuAction())
        self.menuDevice.addAction(self.actionReload)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDevice.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NZXQT"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCooling), _translate("MainWindow", "Cooling"))
        self.labelLogo.setText(_translate("MainWindow", "NZXT"))
        self.labelPresetRevert.setText(_translate("MainWindow", "Revert"))
        self.labelEffectSelection.setText(_translate("MainWindow", "Effects Selection:"))
        self.radioButtonPresetLogo.setText(_translate("MainWindow", "N&ZXT Logo"))
        self.radioButtonPresetRing.setText(_translate("MainWindow", "Ring"))
        self.radioButtonPresetBoth.setText(_translate("MainWindow", "Both"))
        self.labelLogoMode.setText(_translate("MainWindow", "default"))
        self.labelRingMode.setText(_translate("MainWindow", "default"))
        self.labelBothMode.setText(_translate("MainWindow", "default"))
        self.label_2.setText(_translate("MainWindow", "Mode Selection:"))
        self.labelPresetAniSpeedLabel.setText(_translate("MainWindow", "Animation Speed: slowest"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2_1), _translate("MainWindow", "Preset"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2_2), _translate("MainWindow", "Smart"))
        self.pushButtonSave.setText(_translate("MainWindow", "SAVE CHANGES"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLighting), _translate("MainWindow", "Lighting"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOverclock), _translate("MainWindow", "Overclocking"))
        self.labelDevDeviceName.setText(_translate("MainWindow", "Device"))
        self.labelDevSerialNo.setText(_translate("MainWindow", "Serial Number"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuDevice.setTitle(_translate("MainWindow", "&Device"))
        self.menu_Select_Device.setTitle(_translate("MainWindow", "&Select Device:"))
        self.actionReload.setText(_translate("MainWindow", "&Refresh Devices"))
        self.actiondummy.setText(_translate("MainWindow", "&dummy"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Sa&ve As..."))
        self.actionOpen.setText(_translate("MainWindow", "&Open..."))
        self.actionNew.setText(_translate("MainWindow", "&New Profile"))
        self.actionReset.setText(_translate("MainWindow", "&Reset"))
        self.actionExit.setText(_translate("MainWindow", "&Exit"))

from PyQt5 import QtChart
