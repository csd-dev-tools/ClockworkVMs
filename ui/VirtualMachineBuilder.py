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
        btnTwo = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Apply)
        btnTwo.clicked.connect(self.installPacker)
        btnTwo.hide()

        self.chkApp = CheckApplicable(self.environ, self.logger)
        self.macOsBlackListApplicable = {'type': 'black', 'os': {'Mac OS X': ['10.0.0', 'r', '20.12.10']}}
        self.linuxWhitelistApplicable = {'type' : 'white', 'family' : 'linux'}
        self.freebsdWhitelistApplicable = {'type' : 'white', 'family' : 'freebsd'}
        self.macosWhitelistApplicable = {'type' : 'white', 'family' : 'darwin'}
        #openbsdWhitelistApplicable = {}
        #windowsWhitelistApplicable = {}

        #####
        # Set up the configure dialog
        self.configRepos = ConfigureRepos(self.conf)
        self.configRepos.setWindowTitle("Configure Repos")

        #####
        # Connect the configure 'done' signal to the refreshFamilyComboBox slot
        self.configRepos.doneConfigure.connect(self.refreshFamilyComboBox)

        #####
        # Signal/slot to deal with osFamily combo box change
        self.ui.osFamily.currentIndexChanged.connect(self.osFamilySelected)        
        
        self.refreshFamilyComboBox()
        self.osFamilySelected(0)

        self.logger.log(lp.DEBUG, "Done with VirtualMachineBuilder init...")
        
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

    def refreshFamilyComboBox(self):
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

        self.logger.log(lp.DEBUG, str(self.osSavailable))

        #####
        # temporarily disconnect Signal/slot to deal with osFamily combo box
        #
        # It appears that adding values to the combo box changes the combo
        # box index, which throws the currentIndexChanged signal, therefore
        # we have to disconnect the signal, add the combo box values, then
        # set up the signal again.
        #
        self.ui.osFamily.currentIndexChanged.disconnect(self.osFamilySelected)

        if self.osSavailable:
            self.osComboBoxValues = []
            self.ui.osFamily.clear()
            self.ui.osFamily.addItems(self.osSavailable)
            self.osComboBoxValues += self.osSavailable
        else:
            self.configureRepos()
            return 0

        self.logger.log(lp.DEBUG, str(self.osComboBoxValues))

        self.osVersComboBox = {}
        repoPaths = []
        files = []

        self.logger.log(lp.DEBUG, str(self.osComboBoxValues))

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
            files = []
        self.logger.log(lp.DEBUG, str(self.osVersComboBox))

        #####
        # Signal/slot to deal with osFamily combo box change
        self.ui.osFamily.currentIndexChanged.connect(self.osFamilySelected)        

    def osFamilySelected(self, index):
        """
        Traslate a combobox position to a string.

        @author: Roy Nielsen
        """
        self.ui.osVersions.clear()

        self.logger.log(lp.DEBUG, "Index: " + str(index))

        if -1 == index :
            index = 0

        indexText = self.ui.osFamily.itemText(index).strip()

        self.logger.log(lp.DEBUG, str(indexText))

        for osVersVarsFile in self.osVersComboBox[indexText]:
            self.logger.log(lp.DEBUG, str(osVersVarsFile))
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
        ""
        #####
        # Check if /usr/local/bin/packer already exists
        
        if not os.path.exists("/usr/local/bin/packer"):
            #####
            # Check hardware
            try:
                sysname, nodename, release, version, machine = os.uname()
            except Exception, err:
                raise err
            
            #####
            # determine the correct download URL for packer
            #
            # Need method to auto-detect lates version from the repo and auto-select the right one.
            #
            if re.match("x86_64", str(machine)) and linuxWhitelistApplicable:
                packerDownloadUrl = "https://releases.hashicorp.com/packer/1.0.2/packer_1.0.2_linux_386.zip"
            elif re.match("i386", str(machine)) and linuxWhitelistApplicable:
                packerDownloadUrl = "https://releases.hashicorp.com/packer/1.0.2/packer_1.0.2_linux_amd64.zip"
            elif re.match("x86_64", str(machine)) and macosWhitelistApplicable:
                packerDownloadUrl = "https://releases.hashicorp.com/packer/1.0.2/packer_1.0.2_darwin_amd64.zip"
            elif re.match("i386", str(machine)) and macosWhitelistApplicable:
                packerDownloadUrl = "https://releases.hashicorp.com/packer/1.0.2/packer_1.0.2_darwin_386.zip"
    
            #####
            # Download package
            
            #####
            # Install package
            
            #####
            # Check ownership and permissions
            
            """
