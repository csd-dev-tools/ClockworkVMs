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
from lib.CheckApplicable import CheckApplicable
from lib.environment import Environment
from lib.libHelperFunctions import isSaneFilePath

#####
# Import pyuic5 compiled PyQt ui files
from ui.ConfigureRepos_ui import Ui_Dialog
from ui.PrepareIso import PrepareIso
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


class ConfigureRepos(QtWidgets.QDialog):
    """
    Class to manage the set password dialog...

    @author: Roy Nielsen
    """

    doneConfigure = QtCore.pyqtSignal()
    
    def __init__(self, conf, parent=None):
        """
        Initialization method...

        @author: Roy Nielsen
        """
        super(ConfigureRepos, self).__init__(parent)

        self.ui =  Ui_Dialog()
        self.ui.setupUi(self)

        #####
        # initialization of class variables.
        self.conf = conf
        self.environ = Environment()
        self.conf.loggerSelf()
        self.logger = self.conf.getLogger()
        #self.logger = self.conf.get_logger()
        self.logger.log(lp.DEBUG, str(self.logger))
        self.runWith = RunWith(self.logger)
        self.libc = getLibc(self.logger)
        self.chkApp = CheckApplicable(self.environ, self.logger)
        macOsWhiteListApplicable = {'type': 'white', 'os': {'Mac OS X': ['10.0.0', 'r', '20.12.10']}}

        #####
        # Handle button box
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close) 
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.okDone) 

        #####
        # Handle other buttons
        self.ui.downloadReposButton.clicked.connect(self.downloadRepos)
        self.ui.prepareIsoButton.clicked.connect(self.prepareIso)
        self.ui.gitResetHardButton.clicked.connect(self.resetRepos)
        self.ui.gitPullButton.clicked.connect(self.updateRepos)
        
        if self.chkApp.isApplicable(macOsWhiteListApplicable):
            self.ui.prepareIsoButton.clicked.connect(self.prepareIso)
        else:
            self.ui.prepareIsoButton.hide()
            self.ui.macosCheckBox.hide()

        #####
        # default boxcutter repo path
        self.reposRoot = self.conf.getRepoRoot()
        
        #####
        # Future features
        self.ui.winCheckBox.hide()
        self.ui.label_2.hide()
        self.ui.leReposPath.hide()
        self.ui.proxyButton.hide()

        #####
        # Future features
        self.ui.winCheckBox.hide()
        self.ui.label_2.hide()
        self.ui.leReposPath.hide()
        self.ui.proxyButton.hide()

        self.git = "/usr/bin/git"
        
        #####
        # repos
        self.repos2process = []
        
        self.getSelected()

    def okDone(self):
        '''
        '''
        self.getSelected()
        
        #####
        # Validate that the repos selected have a directory in the reporoot
        if self.repos2process:
            for repo in self.repos2process:
                if not os.path.isdir(repo):
                    break
            self.processGitCommand('clone')
        
        self.doneConfigure.emit()
        self.accept

    def getSelected(self):
        '''
        '''
        if self.ui.debianCheckBox.isChecked():
            self.repos2process.append("debian")
        if self.ui.ubuntuCheckBox.isChecked():
            self.repos2process.append("ubuntu")
        if self.ui.bsdCheckBox.isChecked():
            self.repos2process.append("bsd")
        if self.ui.macosCheckBox.isChecked():
            self.repos2process.append("macos")
        if self.ui.fedoraCheckBox.isChecked():
            self.repos2process.append("fedora")
        if self.ui.centosCheckBox.isChecked():
            self.repos2process.append("centos")
        if self.ui.oracleCheckBox.isChecked():
            self.repos2process.append("oraclelinux")
        if self.ui.winCheckBox.isChecked():
            self.repos2process.append("windows")

        self.logger.log(lp.DEBUG, "Repos to process: " + str(self.repos2process))
        
    def downloadRepos(self, subcommand=""):
        '''
        Slot to determine how to process the download repos button

        @author: Roy Nielsen
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Downloading repos...", QtWidgets.QMessageBox.Ok)
        self.processGitCommand("clone")

    def resetRepos(self):
        '''
        Slot to determine how to reset repos via the git reset --hard button

        @author: Roy Nielsen
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Resetting repos...", QtWidgets.QMessageBox.Ok)
        self.processGitCommand(["reset", "--hard"])

    def updateRepos(self):
        '''
        Slot to determine how to update repos via the git pull button

        @author: Roy Nielsen
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Updating repos...", QtWidgets.QMessageBox.Ok)
        self.processGitCommand("pull")

    def processGitCommand(self, subcommand=""):
        '''
        Process the git commands via the appropriately called slot

        @author: Roy Nielsen
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Processing Repos...", QtWidgets.QMessageBox.Ok)
        repos2process = []

        self.getSelected()

        #####
        # mkdirs reporoot 
        if not os.path.exists(self.reposRoot):
            try:
                os.makedirs(self.reposRoot)
            except OSError, err:
                self.logger.log(lp.INFO, traceback.format_exc())
                raise(err)

        #####
        # Get and set the proxy if there is one
        shellEnviron = os.environ.copy()
        proxy = self.conf.getProxy()
        httpsProxy = self.conf.getHttpsProxy()
        httpProxy = self.conf.getHttpProxy()
        ftpProxy = self.conf.getFtpProxy()
        rsyncProxy = self.conf.getRsyncProxy()
        noProxy = self.conf.getNoProxy()

        if proxy and isinstance(proxy, basestring):
            shellEnviron['http_proxy'] = proxy
            shellEnviron['https_proxy'] = proxy
            shellEnviron['ftp_proxy'] = proxy
            shellEnviron['rsync_proxy'] = proxy
        if httpProxy and isinstance(httpProxy, basestring):
            shellEnviron['http_proxy'] = httpProxy
        if httpsProxy and isinstance(httpsProxy, basestring):
            shellEnviron['https_proxy'] = httpsProxy
        if ftpProxy and isinstance(ftpProxy, basestring):
            shellEnviron['ftp_proxy'] = ftpProxy
        if rsyncProxy and isinstance(rsyncProxy, basestring):
            shellEnviron['rsync_proxy'] = rsyncProxy
        if noProxy and isinstance(noProxy, basestring):
            shellEnviron['no_proxy'] = noProxy

        #####
        # loop through repos and download the ones that have been checked.
        for repo in self.repos2process:
            if not os.path.exists(self.reposRoot + "/" + repo):
                subcommand = "clone"
            returnDir = os.getcwd()
            if not 'clone' == subcommand:
                os.chdir(self.reposRoot + "/" + repo)
            else:
                os.chdir(self.reposRoot)
            self.logger.log(lp.DEBUG, str(os.getcwd()))
            
            #####
            # Assign the right "subcommand" to the command to be processed
            if isinstance(subcommand, basestring) and subcommand:
                if re.match("clone", subcommand):
                    cmd = [self.git, subcommand, "https://github.com/boxcutter/" + repo +".git"]
                else:
                    cmd = [self.git, subcommand]
            if isinstance(subcommand, list) and subcommand:
                cmd = [self.git] + subcommand

            #####
            # Set and execute the built command
            self.runWith.setCommand(cmd, env=shellEnviron)
            output, error, retcode = self.runWith.communicate()

            self.logger.log(lp.DEBUG, "OUT: " + str(output))
            self.logger.log(lp.DEBUG, "ERR: " + str(error))
            self.logger.log(lp.DEBUG, "RETCODE: " + str(retcode))

            os.chdir(returnDir)

    def prepareIso(self):
        '''
        
        @author: Roy Nielsen
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Prepare a disk image for creating a macOS VM...", QtWidgets.QMessageBox.Ok)

        mydialog = PrepareIso(self.conf)
        #mydialog.setOpenExternalLinks(True)
        #mydialog.setModal(True)
        #mydialog.setWindowTitle("Virtual Machine Builder")
        mydialogRetval = mydialog.exec_()
        mydialog.raise_()

