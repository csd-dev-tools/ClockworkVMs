# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/PrepareIso.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PrepareMacosImage(object):
    def setupUi(self, PrepareMacosImage):
        PrepareMacosImage.setObjectName("PrepareMacosImage")
        PrepareMacosImage.resize(627, 302)
        self.gridLayout = QtWidgets.QGridLayout(PrepareMacosImage)
        self.gridLayout.setObjectName("gridLayout")
        self.bOpenInstallerApp = QtWidgets.QPushButton(PrepareMacosImage)
        self.bOpenInstallerApp.setObjectName("bOpenInstallerApp")
        self.gridLayout.addWidget(self.bOpenInstallerApp, 5, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(PrepareMacosImage)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(PrepareMacosImage)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(PrepareMacosImage)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(PrepareMacosImage)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.leInstallAppLocation = QtWidgets.QLineEdit(PrepareMacosImage)
        self.leInstallAppLocation.setObjectName("leInstallAppLocation")
        self.gridLayout.addWidget(self.leInstallAppLocation, 5, 0, 1, 2)
        self.bPrepareIso = QtWidgets.QPushButton(PrepareMacosImage)
        self.bPrepareIso.setObjectName("bPrepareIso")
        self.gridLayout.addWidget(self.bPrepareIso, 6, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(PrepareMacosImage)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 2)
        self.label = QtWidgets.QLabel(PrepareMacosImage)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(PrepareMacosImage)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(PrepareMacosImage)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        self.retranslateUi(PrepareMacosImage)
        self.buttonBox.accepted.connect(PrepareMacosImage.accept)
        self.buttonBox.rejected.connect(PrepareMacosImage.reject)
        QtCore.QMetaObject.connectSlotsByName(PrepareMacosImage)

    def retranslateUi(self, PrepareMacosImage):
        _translate = QtCore.QCoreApplication.translate
        PrepareMacosImage.setWindowTitle(_translate("PrepareMacosImage", "Dialog"))
        self.bOpenInstallerApp.setText(_translate("PrepareMacosImage", "Open"))
        self.label_4.setText(_translate("PrepareMacosImage", "Create and Image packer can use to create a Virtual Machine"))
        self.label_2.setText(_translate("PrepareMacosImage", "Download the latest - 1 version of <a href=\"https://itunes.apple.com/app/os-x-el-capitan/id1147835434?mt=12\">macOS</a>"))
        self.label_3.setText(_translate("PrepareMacosImage", "macOS Install App location"))
        self.label_5.setText(_translate("PrepareMacosImage", "prepare_iso.sh"))
        self.bPrepareIso.setText(_translate("PrepareMacosImage", "prepare_iso"))
        self.label_6.setText(_translate("PrepareMacosImage", "Create a macOS disk image that packer can use as a reference to create a macOS Virtual Machine"))
        self.label.setText(_translate("PrepareMacosImage", "Download the latest version of <a href=\"https://itunes.apple.com/us/app/macos-sierra/id1127487414?mt=12&l=en-us#\">macOS</a>"))
        self.label_7.setText(_translate("PrepareMacosImage", "NOTE:  Currently must be completed on a macOS machine"))

