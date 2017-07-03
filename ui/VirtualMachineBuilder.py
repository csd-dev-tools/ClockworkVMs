from __future__ import absolute_import

import os
import re
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
from lib.environment import Environment
from lib.CheckApplicable import CheckApplicable
from lib.libHelperFunctions import isSaneFilePath

#####
# Import pyuic5 compiled PyQt ui files
from ui.VirtualMachineBuilder_ui import  Ui_MainWindow
from ui.VirtualMachineSettings import VirtualMachineSettings
from ui.SettingsOk import SettingsOk
from ui.ConfigureRepos import ConfigureRepos


#####
# Exception for when the conf file can't be grokked.
class ConfusingConfigurationError(Exception):
    """
    Meant for being thrown when the the application can't determine
    configuration information.

    @author: Roy Nielsen
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class VirtualMachineBuilder(QtWidgets.QMainWindow):
    """
    Class to manage the dialog...

    @author: Roy Nielsen
    """
    def __init__(self, conf, parent=None):
        """
        Initialization method...

        @author: Roy Nielsen
        """
        super(VirtualMachineBuilder, self).__init__(parent)

        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)

        #####
        # initialization of class variables.
        self.conf = conf
        self.conf.loggerSelf()
        self.logger = self.conf.getLogger()
        self.environ = Environment()
        #self.logger = self.conf.get_logger()
        self.logger.log(lp.DEBUG, str(self.logger))
        self.runWith = RunWith(self.logger)
        self.libc = getLibc(self.logger)

        #####
        # Set label states
        self.ui.packerLabel.setText("( <a href='https://www.packer.io'>https://www.packer.io</a> - Download and install packer separately )")
        self.ui.boxcutterLabel.setText("( <a href='https://github.com/boxcutter'>https://github.com/boxcutter</a> - Clone repos separately )")

        #####
        # Handle button box
        #
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(self.closeApplication) 
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.processVm) 

        #####
        # Rename Save button
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setText("Configure Repos")
        btn = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
        btn.clicked.connect(self.configureRepos)

        #####
        # Rename Apply button
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setText("Install packer")
        btn = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Apply)
        btn.clicked.connect(self.installPacker)
        self.ui.buttonBox.apply.hide()

        #####
        # Set up the configure dialog
        self.configRepos = ConfigureRepos(self.conf)
        self.configRepos.setWindowTitle("Configure Repos")

        #####
        # Connect the configure 'done' signal to the refreshComboBoxes slot
        self.configRepos.doneConfigure.connect(self.refreshComboBoxes)

        self.chkApp = CheckApplicable(self.environ, self.logger)
        self.macOsBlackListApplicable = {'type': 'black', 'os': {'Mac OS X': ['10.0.0', 'r', '20.12.10']}}

        self.refreshComboBoxes()

    def refreshComboBoxes(self):
        '''
        Determine what to put in the ComboBoxes
        '''
        #####
        # Fill the OS combo box
        validOSs = ["debian", "ubuntu", "bsd", "macos",
                    "fedora", "centos", "oraclelinux"]
        if self.chkApp.isApplicable(self.macOsBlackListApplicable):
            validOSs.remove('macos')

        self.repoRoot = self.conf.getRepoRoot()

        try:
            self.osSavailable = os.listdir(self.repoRoot)
        except OSError, err:
            os.makedirs(self.repoRoot)
            self.osSavailable = os.listdir(self.repoRoot)

        self.osComboBoxValues = []

        if self.osSavailable:
            for myos in self.osSavailable:
                if myos in validOSs:
                    self.osComboBoxValues.append(myos)
                    self.ui.osFamily.addItem(myos)
        else:
            self.configureRepos()

        self.ui.osFamily.currentIndexChanged.connect(self.osFamilySelected)
        
        self.osVersComboBox = {}
        
        repoPaths = []
        files = []

        for mydir in self.osComboBoxValues:
            mydirlist = os.listdir(self.conf.getRepoRoot() + "/" + mydir)
            for item in mydirlist:
                if re.match("^\w+\d+.*\.json", item) and \
                   re.search("%s"%mydir, item):
                    files.append(item)
                    self.logger.log(lp.DEBUG, str(item))
                elif re.match("^ol\d+.*\.json", item):
                    files.append(item)
                    self.logger.log(lp.DEBUG, str(item))
                elif re.match("^win.*\.json", item):
                    files.append(item)
                    self.logger.log(lp.DEBUG, str(item))
                    
            self.osVersComboBox[mydir] = files
            self.logger.log
            files = []
        self.osFamilySelected(0)
        
    def setOpenExternalLinks(self, set_state=True):
        """
        Use the OS method of opening Links

        @author: Roy Nielsen
        """
        success = False
        if isinstance(set_state, bool):
            if set_state is True:
                self.ui.packerLabel.setOpenExternalLinks(True)
                self.ui.boxcutterLabel.setOpenExternalLinks(True)
                self.logger.log(lp.DEBUG, "Browser links activated...")
                success = True
            else:
                self.ui.packerLabel.setOpenExternalLinks(False)
                self.ui.boxcutterLabel.setOpenExternalLinks(False)
                self.logger.log(lp.DEBUG, "Browser links deactivated...")
                success = True
        else:
            self.logger.log(lp.WARNING, "Invalid value passed in to " + \
                                        "this method: " + str(set_state))

        return success

    def osFamilySelected(self, index):
        """
        Traslate a combobox position to a string.

        @author: Roy Nielsen
        """
        self.ui.osVersions.clear()
        self.logger.log(lp.DEBUG, "Index: " + str(index))
        
        indexText = self.ui.osFamily.itemText(index)
        for osVersVarsFile in self.osVersComboBox[indexText]:
            self.ui.osVersions.addItem(osVersVarsFile)

    def configureRepos(self):
        """
        Spawn the ConfigureRepos interface.

        @author: Roy Nielsen
        """
        QtWidgets.QMessageBox.information(self, "Information", "...Configuring Repos...", QtWidgets.QMessageBox.Ok)

        #####
        # Raise the configRepos dialog
        self.configRepos.exec_()
        self.configRepos.raise_()

    def processVm(self):
        """
        Set the configuration and spawn the VirtualMachineSettings interface

        @author: Roy Nielsen
        """
        QtWidgets.QMessageBox.information(self, "Information", "...Processing VM...", QtWidgets.QMessageBox.Ok)

        currentOs = self.ui.osFamily.currentText()
        currentVarFile = self.ui.osVersions.currentText()

        varFileFullPath = self.conf.getRepoRoot() + "/" + currentOs + "/" + currentVarFile
        repo = self.conf.getRepoRoot() + "/" + currentOs

        if not re.match("^ol", currentVarFile):
            templateFileRegex = re.match("^([A-Za-z_\-]+)\d+.*\.json$", currentVarFile)
            templateFile = templateFileRegex.group(1) + ".json"
        else:
            templateFile = "oraclelinux.json"

        templateFilePath = self.conf.getRepoRoot() + "/" + currentOs + "/" + templateFile
        self.logger.log(lp.DEBUG, "TemplateFilePath: " + str(templateFilePath))

        self.conf.setCurrentVarFilePath(varFileFullPath)
        self.conf.setCurrentTemplateFilePath(templateFilePath)
        self.conf.setCurrentRepo(repo)

        #####
        # Set up dialog
        vmSettings = VirtualMachineSettings(self.conf)
        vmSettings.setWindowTitle("Configure Repos")
        #workConfig.show()
        vmStngRetval = vmSettings.exec_()
        vmSettings.raise_()
        
    def closeApplication(self):
        """
        """
        self.closeAllWindows()

    def installPacker(self):
        """
        """
        pass
