from __future__ import absolute_import

import os
import re
import sys
import time
import urllib
import shutil
import httplib
import traceback
import subprocess

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
from lib.libHelperFunctions import isSaneFilePath
from lib.run_commands import runMyThreadCommand
from lib.packerJsonHandler import PackerJsonHandler
#####
# Import pyuic5 compiled PyQt ui files
from ui.PrepareIso_ui import Ui_PrepareMacosImage
from ui.admin_creds import AdministratorCredentials

class PrepareIso(QtWidgets.QDialog):
    """
    Class to manage the prepare_iso dialog...

    @author: Roy Nielsen
    """
    def __init__(self, conf, parent=None):
        """
        Initialization method...

        @author: Roy Nielsen
        """
        super(PrepareIso, self).__init__(parent)

        self.ui =  Ui_PrepareMacosImage()
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
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject) 
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept) 

        #####
        # Handle other buttons
        self.ui.bOpenInstallerApp.clicked.connect(self.openInstallerApp)
        self.ui.bPrepareIso.clicked.connect(self.prepareIso)

        #####
        # Set up collection of administrator credentials
        self.adminCreds = AdministratorCredentials(self.conf)
        self.adminCreds.creds.connect(self.setUserAndPass)
        
        #####
        # Instanciate a PackerJsonHandler
        self.pjh = PackerJsonHandler(self.logger)

    def setUserAndPass(self, user="", password=""):
        '''
        '''
        self.username = user.strip()
        self.password = password.strip()    

    def openInstallerApp(self):
        '''
        '''
        self.installerApp = ""

        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', "/Applications", "Install*")

        if not os.path.isdir(fname) or not re.match(".*\.app$", fname):
            #####
            # Throw an error
            QtWidgets.QMessageBox.critical(self, "Error", "...Not a valid installer Application...", QtWidgets.QMessageBox.Ok)
        else:
            self.ui.leInstallAppLocation.setText(fname)
            self.installerApp = re.sub(" ", "\\\\\ ", fname.strip())
            #self.installerApp = fname.strip()
            self.logger.log(lp.DEBUG, "installerApp: " + str(self.installerApp))

    def prepareIso(self):
        '''
        The commands to create the disk image packer can use are:
        cd ~boxcutter/macos
        sudo prepare_iso/prepare_iso.sh /Applications/Install\ OS\ X\ El\ Capitan.app dmg
        "do shell script \"/Applications/stonix4mac.app/Contents/Resources/stonix.app/Contents/MacOS/stonix > /dev/null 2>&1 &\" with administrator privileges"
        '''
        adminCredsReturns = self.adminCreds.exec_()
        self.adminCreds.raise_()

        returnDir = os.getcwd()
        os.chdir(self.conf.getRepoRoot() + "/macos")
        print os.getcwd()

        subcmd = """./prepare_iso/prepare_iso.sh %s dmg"""%(self.installerApp) 

        cmd = ["/usr/bin/osascript", "-e", "do shell script \"{0}\" user name \"{1}\" password \"{2}\" with administrator privileges".format(subcmd, self.username, self.password)]

        self.runWith.setCommand(cmd, myshell=False)

        output, error, retcode = self.runWith.waitNpassThruStdout()

        self.logger.log(lp.DEBUG, "out: " + str(output))
        self.logger.log(lp.DEBUG, "err: " + str(error))
        self.logger.log(lp.DEBUG, "retcode: " + str(retcode))

        #####
        # Get the (\w+_InstallESD_\w+\.dmg) name out of the output to write it
        # into the appropriate varfile
        compile_dmg_name = re.compile(".*(OSX_InstallESD_[\d\.]+_\w+\.dmg).*")
        dmgName = ""
        for line in output.split("\n"):
            try:
                search = compile_dmg_name.search(line)
                dmgName = search.group(1)
                break
            except KeyError, err:
                pass
                # self.logger.log(lp.DEBUG, traceback.format_exc(err))

        #####
        # Get the version out of the above variable to determine the right
        # varfile to write to.
        dmgVersSearch = re.search("OSX_InstallESD_(\d+\.\d+)\..*_\w+\.dmg", dmgName)
        dmgVersion = ""
        try:
            dmgVersion = dmgVersSearch.group(1)
        except KeyError, err:
            self.logger.log(lp.DEBUG, traceback.format_exc(err))

        dmgVersion = re.sub("\.", "", dmgVersion)
        varfileName = "macos" + str(dmgVersion) + ".json"

        #####
        # Open the var file and acquire its JSON
        varJson = self.pjh.readExistingJsonVarfile(varfileName)

        #####
        # Set eh JSON
        varJson["iso_url"] = self.conf.getRepoRoot() + "/macos/dmg/" + dmgName

        #####
        # Save the new JSON
        self.pjh.saveJsonVarFile(varfileName, varJson)

        self.libc.sync()

        os.chdir(returnDir)

    def saveImage(self):
        '''
        '''
        self.macOSPath = self.conf.getRepoRoot().strip() + "/macos/dmg"
        QtWidgets.QFileDialog.getSaveFileName(self, 'macOS Image', self.macOSPath, selectedFilter='*.dmg')
