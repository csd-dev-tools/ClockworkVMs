# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ConfigureRepos.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 270)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.winCheckBox = QtWidgets.QCheckBox(Dialog)
        self.winCheckBox.setObjectName("winCheckBox")
        self.gridLayout.addWidget(self.winCheckBox, 5, 1, 1, 1)
        self.bsdCheckBox = QtWidgets.QCheckBox(Dialog)
        self.bsdCheckBox.setObjectName("bsdCheckBox")
        self.gridLayout.addWidget(self.bsdCheckBox, 4, 0, 1, 1)
        self.oracleCheckBox = QtWidgets.QCheckBox(Dialog)
        self.oracleCheckBox.setObjectName("oracleCheckBox")
        self.gridLayout.addWidget(self.oracleCheckBox, 4, 1, 1, 1)
        self.macosCheckBox = QtWidgets.QCheckBox(Dialog)
        self.macosCheckBox.setObjectName("macosCheckBox")
        self.gridLayout.addWidget(self.macosCheckBox, 5, 0, 1, 1)
        self.centosCheckBox = QtWidgets.QCheckBox(Dialog)
        self.centosCheckBox.setObjectName("centosCheckBox")
        self.gridLayout.addWidget(self.centosCheckBox, 3, 1, 1, 1)
        self.debianCheckBox = QtWidgets.QCheckBox(Dialog)
        self.debianCheckBox.setObjectName("debianCheckBox")
        self.gridLayout.addWidget(self.debianCheckBox, 1, 0, 1, 1)
        self.fedoraCheckBox = QtWidgets.QCheckBox(Dialog)
        self.fedoraCheckBox.setObjectName("fedoraCheckBox")
        self.gridLayout.addWidget(self.fedoraCheckBox, 1, 1, 1, 1)
        self.downloadReposButton = QtWidgets.QPushButton(Dialog)
        self.downloadReposButton.setObjectName("downloadReposButton")
        self.gridLayout.addWidget(self.downloadReposButton, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.ubuntuCheckBox = QtWidgets.QCheckBox(Dialog)
        self.ubuntuCheckBox.setObjectName("ubuntuCheckBox")
        self.gridLayout.addWidget(self.ubuntuCheckBox, 3, 0, 1, 1)
        self.prepareIsoButton = QtWidgets.QPushButton(Dialog)
        self.prepareIsoButton.setObjectName("prepareIsoButton")
        self.gridLayout.addWidget(self.prepareIsoButton, 3, 2, 1, 1)
        self.gitResetHardButton = QtWidgets.QPushButton(Dialog)
        self.gitResetHardButton.setObjectName("gitResetHardButton")
        self.gridLayout.addWidget(self.gitResetHardButton, 4, 2, 1, 1)
        self.gitPullButton = QtWidgets.QPushButton(Dialog)
        self.gitPullButton.setObjectName("gitPullButton")
        self.gridLayout.addWidget(self.gitPullButton, 5, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.leReposPath = QtWidgets.QLineEdit(Dialog)
        self.leReposPath.setObjectName("leReposPath")
        self.gridLayout.addWidget(self.leReposPath, 6, 1, 1, 2)
        self.proxyButton = QtWidgets.QPushButton(Dialog)
        self.proxyButton.setObjectName("proxyButton")
        self.gridLayout.addWidget(self.proxyButton, 0, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.winCheckBox.setText(_translate("Dialog", "Windows"))
        self.bsdCheckBox.setText(_translate("Dialog", "BSD"))
        self.oracleCheckBox.setText(_translate("Dialog", "Oracle"))
        self.macosCheckBox.setText(_translate("Dialog", "macOS"))
        self.centosCheckBox.setText(_translate("Dialog", "Centos"))
        self.debianCheckBox.setText(_translate("Dialog", "Debian"))
        self.fedoraCheckBox.setText(_translate("Dialog", "Fedora"))
        self.downloadReposButton.setText(_translate("Dialog", "Download Repos"))
        self.label.setText(_translate("Dialog", "Configure Repos"))
        self.ubuntuCheckBox.setText(_translate("Dialog", "Ubuntu"))
        self.prepareIsoButton.setText(_translate("Dialog", "prepare_iso"))
        self.gitResetHardButton.setToolTip(_translate("Dialog", "Revert all the changes back to the last git checkin"))
        self.gitResetHardButton.setText(_translate("Dialog", "git reset --hard"))
        self.gitPullButton.setToolTip(_translate("Dialog", "Get the newest files from the boxcutter repos"))
        self.gitPullButton.setText(_translate("Dialog", "git pull"))
        self.label_2.setText(_translate("Dialog", "Repos Path"))
        self.proxyButton.setText(_translate("Dialog", "proxy setup"))

