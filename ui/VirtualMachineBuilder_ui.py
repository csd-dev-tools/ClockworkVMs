# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/VirtualMachineBuilder.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(325, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.packerLabel = QtWidgets.QLabel(self.centralwidget)
        self.packerLabel.setObjectName("packerLabel")
        self.gridLayout.addWidget(self.packerLabel, 1, 0, 1, 1)
        self.boxcutterLabel = QtWidgets.QLabel(self.centralwidget)
        self.boxcutterLabel.setObjectName("boxcutterLabel")
        self.gridLayout.addWidget(self.boxcutterLabel, 2, 0, 1, 1)
        self.osFamily = QtWidgets.QComboBox(self.centralwidget)
        self.osFamily.setObjectName("osFamily")
        self.gridLayout.addWidget(self.osFamily, 3, 0, 1, 1)
        self.osVersions = QtWidgets.QComboBox(self.centralwidget)
        self.osVersions.setObjectName("osVersions")
        self.gridLayout.addWidget(self.osVersions, 4, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setToolTipDuration(30)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 325, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "Virtual Machine Builder"))
        self.packerLabel.setText(_translate("MainWindow", "TextLabel"))
        self.boxcutterLabel.setText(_translate("MainWindow", "TextLabel"))

