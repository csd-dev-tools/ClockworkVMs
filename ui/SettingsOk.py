from __future__ import absolute_import

import os
import sys
import time
import urllib
import shutil
import httplib
import traceback
from subprocess import Popen, PIPE
from ConfigParser import SafeConfigParser
####
# Importing PyQt functionality
from PyQt5 import QtWidgets, QtCore, QtGui

#####
# Import local shared libraries
from lib.get_libc import getLibc
from lib.loggers import CyLogger
from lib.run_commands import RunWith
from lib.Connectivity import Connectivity
from lib.loggers import LogPriority as lp
from lib.packerJsonHandler import PackerJsonHandler
from lib.packer_runner import PackerRunner
from lib.libHelperFunctions import isSaneFilePath

#####
# Import pyuic5 compiled PyQt ui files
from ui.SettingsOk_ui import Ui_Dialog
from ui.VirtualMachineSettings import VirtualMachineSettings
#from ui.Work import Work


#####
# Exception for when the conf file can't be grokked.
class ConfusingConfigurationError(Exception):
    """
    Meant for being thrown when the MacBuilder can't determine configuration
    information.

    @author: Roy Nielsen
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class SettingsOk(QtWidgets.QDialog):
    """
    Class to manage the set password dialog...

    @author: Roy Nielsen
    """
    def __init__(self, conf, parent=None):
        """
        Initialization method...

        @author: Roy Nielsen
        """
        super(SettingsOk, self).__init__(parent)

        self.ui =  Ui_Dialog()
        self.ui.setupUi(self)

        #####
        # initialization of class variables.
        self.conf = conf
        self.conf.loggerSelf()
        self.logger = self.conf.getLogger()
        #self.logger = self.conf.get_logger()
        self.logger.log(lp.DEBUG, str(self.logger))
        self.runWith = RunWith(self.logger)
        self.libc = getLibc(self.logger)

        #####
        # Handle button box
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close) 
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.processVm) 

        #####
        # Rename Apply button
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setText("Change Vm Settings")
        btn = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Apply)
        btn.clicked.connect(self.deltaVmSettings)

        #####
        # Acquire current json varfile data and print it.
        self.varFilePath = self.conf.getCurrentVarFilePath()
        if self.varFilePath and isSaneFilePath(self.varFilePath):
            try:
                self.pjh = PackerJsonHandler(self.logger)
                jsonData = self.pjh.readExistingJsonVarfile(self.conf.getCurrentVarFilePath())
            except Exception, err:
                QtWidgets.QMessageBox.critical(self, "Error", "...Exception trying to read packer json...", QtWidgets.QMessageBox.Ok)
                self.logger.log(lp.WARNING, traceback.format_exc())
                self.logger.log(lp.WARNING, str(err))
                raise err
            else:
                self.ui.labelVmName.setText(self.pjh.getVmName())
                self.ui.labelDesktop.setText(self.pjh.getDesktop())
                self.ui.labelCpus.setText(self.pjh.getCpus())
                self.ui.labelMemSize.setText(self.pjh.getMemSize())
                self.ui.labelDiskSize.setText(self.pjh.getDiskSize())
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "...Bad path for packer json...", QtWidgets.QMessageBox.Ok)
            self.close()

    def processVm(self):
        '''
        
        @author: Roy Nielsen
        '''
        pr = PackerRunner(self.conf)
        pr.runPackerBoxcutter(self.conf.getCurrentTemplateFilePath(),
                              self.conf.getCurrentVarFilePath(),
                              self.conf.getOnlyVmImage())

    def deltaVmSettings(self):
        '''
        
        @author: Roy Nielsen
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Change VM settings...", QtWidgets.QMessageBox.Ok)
        #####
        # Set up dialog
        vmSettings = VirtualMachineSettings(self.conf)
        vmSettings.setWindowTitle("Configure Repos")
        #workConfig.show()
        vmSettings.exec_()
        vmSettings.raise_()
