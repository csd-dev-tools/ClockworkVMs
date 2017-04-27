# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/SettingsOk.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(257, 299)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.labelVmName = QtWidgets.QLabel(Dialog)
        self.labelVmName.setObjectName("labelVmName")
        self.gridLayout.addWidget(self.labelVmName, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.labelDesktop = QtWidgets.QLabel(Dialog)
        self.labelDesktop.setObjectName("labelDesktop")
        self.gridLayout.addWidget(self.labelDesktop, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.labelCpus = QtWidgets.QLabel(Dialog)
        self.labelCpus.setObjectName("labelCpus")
        self.gridLayout.addWidget(self.labelCpus, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.labelMemSize = QtWidgets.QLabel(Dialog)
        self.labelMemSize.setObjectName("labelMemSize")
        self.gridLayout.addWidget(self.labelMemSize, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.labelDiskSize = QtWidgets.QLabel(Dialog)
        self.labelDiskSize.setObjectName("labelDiskSize")
        self.gridLayout.addWidget(self.labelDiskSize, 5, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Settings Ok?"))
        self.label_2.setText(_translate("Dialog", "VM Name"))
        self.labelVmName.setText(_translate("Dialog", "lableVmName"))
        self.label_3.setText(_translate("Dialog", "Desktop"))
        self.labelDesktop.setText(_translate("Dialog", "labelDesktop"))
        self.label_4.setText(_translate("Dialog", "CPUs"))
        self.labelCpus.setText(_translate("Dialog", "LableCPUs"))
        self.label_5.setText(_translate("Dialog", "Memory Size"))
        self.labelMemSize.setText(_translate("Dialog", "labelMemSize"))
        self.label_6.setText(_translate("Dialog", "Disk Size"))
        self.labelDiskSize.setText(_translate("Dialog", "TextLabel"))

