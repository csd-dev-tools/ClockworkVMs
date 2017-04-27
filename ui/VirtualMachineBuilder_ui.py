# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/VirtualMachineBuilder.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(329, 199)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.osVersions = QtWidgets.QComboBox(Dialog)
        self.osVersions.setObjectName("osVersions")
        self.gridLayout.addWidget(self.osVersions, 4, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.osFamily = QtWidgets.QComboBox(Dialog)
        self.osFamily.setObjectName("osFamily")
        self.gridLayout.addWidget(self.osFamily, 3, 0, 1, 1)
        self.packerLabel = QtWidgets.QLabel(Dialog)
        self.packerLabel.setObjectName("packerLabel")
        self.gridLayout.addWidget(self.packerLabel, 1, 0, 1, 1)
        self.boxcutterLabel = QtWidgets.QLabel(Dialog)
        self.boxcutterLabel.setObjectName("boxcutterLabel")
        self.gridLayout.addWidget(self.boxcutterLabel, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Virtual Machine Builder"))
        self.label.setText(_translate("Dialog", "Virtual Machine Builder"))
        self.packerLabel.setText(_translate("Dialog", "TextLabel"))
        self.boxcutterLabel.setText(_translate("Dialog", "TextLabel"))

