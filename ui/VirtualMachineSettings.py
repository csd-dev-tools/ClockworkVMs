from __future__ import absolute_import

import os
import re
import sys
import copy
import json
import time
import urllib
import shutil
import httplib
import traceback
import tempfile
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

from lib.libHelperFunctions import isSaneFilePath
from lib.packerJsonHandler import PackerJsonHandler
from lib.packer_runner import PackerRunner

#####
# Import pyuic5 compiled PyQt ui files
from ui.VMSettings_ui import Ui_VmSettings_ui
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


class VirtualMachineSettings(QtWidgets.QDialog):
    """
    Class to manage the set password dialog...

    @author: Roy Nielsen
    """
    def __init__(self, conf, parent=None):
        """
        Initialization method...

        @author: Roy Nielsen
        """
        super(VirtualMachineSettings, self).__init__(parent)

        self.ui =  Ui_VmSettings_ui()
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
        self.vPjh = PackerJsonHandler(self.logger) # variables file
        self.tPjh = PackerJsonHandler(self.logger) # template file
        self.jsonData = {}
        self.vmTypes = []
        self.doVagrantBox = False
        self.vmSelected = False

        ####################
        ### TEMPORARY until functionality is supported
        self.ui.userButton.hide()
        self.ui.proxiesButton.hide()
        ####################

        #####
        # Attempt to reset button roles
        self.ui.openJsonBtn = QtWidgets.QPushButton("Open Json")
        self.ui.openJsonBtn.clicked.connect(self.loadPreviousFile) 
        self.ui.buttonBox.addButton(self.ui.openJsonBtn, QtWidgets.QDialogButtonBox.ActionRole)


        #####
        # Handle button box
        #self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject) 

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.processVm) 

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveForLater) 

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.resetToDefault) 

        #####
        # buttons for the stacked widget.
        self.ui.generalButton.clicked.connect(self.selectGeneral)
        self.ui.isoButton.clicked.connect(self.selectIso)
        self.ui.hardwareButton.clicked.connect(self.selectHardware)
        self.ui.userButton.clicked.connect(self.selectUser)
        self.ui.proxiesButton.clicked.connect(self.selectProxies)

        #####
        # Acquire current json varfile data and print it.
        self.varFilePath = self.conf.getCurrentVarFilePath()
        self.templateFilePath = ""
        self.workingDir = os.path.abspath(os.path.dirname(self.varFilePath))
        self.logger.log(lp.DEBUG, ".")
        self.logger.log(lp.DEBUG, ".")
        self.logger.log(lp.DEBUG, ".")
        self.logger.log(lp.DEBUG, "Working dir: " + str(self.workingDir))
        self.logger.log(lp.DEBUG, ".")
        self.logger.log(lp.DEBUG, ".")
        self.logger.log(lp.DEBUG, ".")
        self.loadValuesToUI(self.varFilePath)
        self.selectGeneral()

    def selectGeneral(self):
        '''
        '''
        self.ui.stackedWidget.setCurrentIndex(0)

    def selectIso(self):
        '''
        '''
        self.ui.stackedWidget.setCurrentIndex(1)

    def selectHardware(self):
        '''
        '''
        self.ui.stackedWidget.setCurrentIndex(2)

    def selectUser(self):
        '''
        '''
        self.ui.stackedWidget.setCurrentIndex(3)

    def selectProxies(self):
        '''
        '''
        self.ui.stackedWidget.setCurrentIndex(4)

    def loadValuesToUI(self, loadfile=""):
        '''
        Load a json file of variables into the interface
        '''
        self.logger.log(lp.DEBUG, "Load File: " + str(loadfile))
        if self.varFilePath and isSaneFilePath(self.varFilePath):
            try:
                self.vJsonData = self.vPjh.readExistingJsonVarfile(loadfile)
                self.logger.log(lp.DEBUG, "JSON loaded: " + str(self.jsonData))
            except Exception, err:
                QtWidgets.QMessageBox.critical(self, "Error", "...Exception trying to read packer json...", QtWidgets.QMessageBox.Ok)
                self.logger.log(lp.WARNING, traceback.format_exc())
                self.logger.log(lp.WARNING, str(err))
                raise err
            else:
                #####
                # Fill out labels
                comment = self.vPjh.getComment()
                templateFile = comment.split()[-1].strip('`')
                templateDir = os.path.dirname(self.varFilePath)
                self.templateFilePath = templateDir + "/" + templateFile
                self.conf.setCurrentTemplateFilePath(self.templateFilePath)
                self.tJsonData = self.tPjh.readExistingJsonTemplateFile(self.templateFilePath)
                #####
                # Turn of checkbox tri-state
                self.ui.chkDesktop.setTristate(False)
                self.ui.chkUpdate.setTristate(False)
                self.ui.chkVmware.setTristate(False)
                self.ui.chkVbox.setTristate(False)
                self.ui.chkParallels.setTristate(False)
                self.ui.chkVagrant.setTristate(False)

                self.loadGuiFromPjh(self.tPjh)
                self.loadGuiFromPjh(self.vPjh)

        else:
            QtWidgets.QMessageBox.critical(self, "Error", "...Bad path for packer json...", QtWidgets.QMessageBox.Ok)
            self.close()

    def loadGuiFromPjh(self, pjh):
        '''
        Load a packer JSON file and insert the values into the interface.
        
        @Note: the user and proxy pannel, while being processed, are not
        currently fully functional.
        
        @param: pjh - PackerJsonHandler appropriate to the file that has been
                      loaded.

        @returns: nothing

        @author: Roy Nielsen
        '''
        ##############################################3
        # stacked widget[0] - general info
        comment = pjh.getComment()
        if comment:
            self.ui.leComment.setText(comment)

        vmName = pjh.getVmName()
        if vmName:
            self.ui.leVmName.setText(vmName)

        #####
        # Fill out desktop and updates
        if re.match("false", pjh.getDesktop()):
            self.ui.chkDesktop.setChecked(False)
        else:
            self.ui.chkDesktop.setChecked(True)

        if re.match("false", pjh.getUpdate()):
            self.ui.chkUpdate.setChecked(False)
        else:
            self.ui.chkUpdate.setChecked(True)

        #####
        # Set image boxes to checked, and read only...
        self.ui.chkVmware.setChecked(False)
        self.ui.chkVbox.setChecked(False)
        self.ui.chkParallels.setChecked(False)
        self.ui.chkVagrant.setChecked(False)

        ##############################################
        # stacked widget[1] - iso info
        isoName = pjh.getIsoName()
        if isoName:
            self.ui.leIsoName.setText(isoName)

        isoChecksum = pjh.getIsoChecksum()
        if isoChecksum:
            self.ui.leIsoHash.setText(isoChecksum)


        isoHashAlgorithm = pjh.getIsoChecksumType()
        if isoHashAlgorithm:
            self.ui.leIsoHashAlgorithm.setText(isoHashAlgorithm)

        isoUrl = pjh.getIsoUrl()
        if isoUrl:
            self.ui.leIsoUrl.setText(isoUrl)

        #####
        # Set the iso path
        varFileDir = os.path.dirname(self.varFilePath)
        isoPath = varFileDir + "/Downloads/"
        if not os.path.exists(isoPath):
            os.mkdir(isoPath)
        elif not os.path.isdir(isoPath):
            #####
            # Move/delete what's there
            pass
        self.ui.leIsoPath.setText(isoPath)
        pjh.setIsoPath(isoPath)

        ##############################################
        # stacked widget[2] - hardware specs
        cpus = pjh.getCpus()
        if cpus:
            self.ui.leCpus.setText(cpus)

        memSize = pjh.getMemSize()
        if memSize:
            self.ui.leMemSize.setText(memSize)

        diskSize = pjh.getDiskSize()
        if diskSize:
            self.ui.leDiskSize.setText(diskSize)

        ##############################################
        # stacked widget[3] - user data
        user = pjh.getSshUser()
        if user:
            self.ui.leUserName.setText(user)

        password = pjh.getSshPassword()
        if password:
            self.ui.leUserPassword.setText(password)
            self.ui.leVerifyPassword.setText(password)

        userComment = pjh.getSshUserComment()
        if userComment:
            self.ui.leUserComment.setText(userComment)

        userHomeDir = pjh.getSshUserHomeDir()
        if userHomeDir:
            self.ui.leUserHomeDir.setText(userHomeDir)

        userShell = pjh.getSshUserShell()
        if userShell:
            self.ui.leUserShell.setText(userShell)

        ##############################################
        # stacked widget[4] - proxy info
        httpProxy = pjh.getHttpProxy()
        confHttpProxy = self.conf.getHttpProxy()
        if confHttpProxy:
            self.ui.leHttpProxy.setText(confHttpProxy)
        elif httpProxy:
            self.ui.leHttpProxy.setText(httpProxy)

        httpsProxy = pjh.getHttpsProxy()
        confHttpsProxy = self.conf.getHttpsProxy()
        if confHttpsProxy:
            self.ui.leHttpsProxy.setText(confHttpsProxy)
        elif httpsProxy:
            self.ui.leHttpsProxy.setText(httpsProxy)

        ftpProxy = pjh.getFtpProxy()
        confFtpProxy = self.conf.getFtpProxy()
        if confFtpProxy:
            self.ui.leFtpProxy.setText(confFtpProxy)
        elif ftpProxy:
            self.ui.leFtpProxy.setText(ftpProxy)

        rsyncProxy = pjh.getRsyncProxy()
        confRsyncProxy = self.conf.getRsyncProxy()
        if confRsyncProxy:
            self.ui.leRsyncProxy.setText(confRsyncProxy)
        elif rsyncProxy:
            self.ui.leRsyncProxy.setText(rsyncProxy)

        noProxy = pjh.getNoProxy()
        confNoProxy = self.conf.getNoProxy()
        if confNoProxy:
            self.ui.leNoProxy.setText(confNoProxy)
        elif noProxy:
            self.ui.leNoProxy.setText(noProxy)

    def clearJsonVariables(self):
        '''
        Clears the self.jsonVariables.  In future, this method may be more 
        complex.
        
        @author: Roy Nielsen
        '''
        self.jsonVariables = {}

    def getVarsFromIface(self):
        '''
        Acquire variables from the GUI

        @author: Roy Nielsen
        '''
        self.jsonVariables = {}
        ##############################################
        # stacked widget[0] - general info

        _comment = self.ui.leComment.text().strip()
        vm_name = self.ui.leVmName.text().strip()

        if _comment:
            self.jsonVariables["_comment"] = _comment
        if vm_name:
            self.jsonVariables["vm_name"] = vm_name

        #####
        # Get checkbox values
        self.jsonVariables["desktop"] = str(self.ui.chkDesktop.isChecked()).lower()
        self.jsonVariables["update"] = str(self.ui.chkUpdate.isChecked()).lower()

        if not self.ui.chkVagrant.isChecked():
            self.only = True
        else:
            self.only = False

        ##############################################3
        # stacked widget[1] - general info
        iso_name = self.ui.leIsoName.text().strip()
        iso_url = self.ui.leIsoUrl.text().strip()
        iso_path = self.ui.leIsoPath.text().strip()
        iso_hash = self.ui.leIsoHash.text().strip()
        iso_hash_algorithm = self.ui.leIsoHashAlgorithm.text().strip()
        if iso_path:
            self.jsonVariables["iso_path"] = iso_path
        if iso_url:
            self.jsonVariables["iso_url"] = iso_url
        if iso_path:
            self.jsonVariables["iso_path"] = iso_path
        if iso_hash:
            self.jsonVariables["iso_checksum"] = iso_hash
        if iso_hash_algorithm:
            self.jsonVariables["iso_checksum_type"] = iso_hash_algorithm

        ##############################################
        # stacked widget[2] - general info
        cpus = self.ui.leCpus.text().strip()
        memory = self.ui.leMemSize.text().strip()
        disk_size = self.ui.leDiskSize.text().strip()

        if cpus:
            self.jsonVariables["cpus"] = cpus
        if memory:
            self.jsonVariables["memory"] = memory
        if disk_size:
            self.jsonVariables["disk_size"] = disk_size

        ##############################################
        # stacked widget[3] - general info
        
        ssh_user = self.ui.leUserName.text().strip()
        ssh_password = self.ui.leUserPassword.text().strip()
        ssh_verify_password = self.ui.leVerifyPassword.text().strip()
        ssh_user_home = self.ui.leUserHomeDir.text().strip()
        ssh_user_shell = self.ui.leUserShell.text().strip()
        ssh_user_comment = self.ui.leUserComment.text().strip()

#loop???

        if ssh_user:
            self.jsonVariables["ssh_username"] = ssh_user
        if ssh_password and ssh_password == ssh_verify_password:
            self.jsonVariables["ssh_password"] = ssh_password
        else:
            self.clearJsonVariables()
            QtWidgets.QMessageBox.critical(self, "Error", "...Password mis-match, please re-enter passwords...", QtWidgets.QMessageBox.Ok)

        ##############################################
        # stacked widget[4] - general info
        self.jsonVariables["http_proxy"] = self.ui.leHttpProxy.text().strip()
        self.jsonVariables["https_proxy"] = self.ui.leHttpsProxy.text().strip()
        self.jsonVariables["ftp_proxy"] = self.ui.leFtpProxy.text().strip()
        self.jsonVariables["rsync_proxy"] = self.ui.leRsyncProxy.text().strip()
        self.jsonVariables["no_proxy"] = self.ui.leNoProxy.text().strip()

        self.logger.log(lp.DEBUG, "JSON data: " + str(self.jsonData))

    def mergeIfaceVarsWithVarFile(self):
        '''
        Merge interface variables with the var file
        
        @author: Roy Nielsen
        '''
        loadFile = self.conf.getCurrentVarFilePath()
        self.jsonVariables = self.vPjh.readExistingJsonVarfile(loadFile)
        self.vPjh.printVariables()
        self.getVarsFromIface()
        #print str(self.jsonVariables)

    def saveTemporaryTemplateFile(self, filename=''):
        '''
        Save a temporary template file to use with the packer command.
        
        @param: filename - name of the file to save.
        
        @author: Roy Nielsen
        '''
        templateFile = self.conf.getCurrentTemplateFilePath()
        vmtypes = []
        includeVagrant = False

        if self.ui.chkVmware.isChecked():
            vmtypes.append('vmware-iso')
        if self.ui.chkVbox.isChecked():
            vmtypes.append('virtualbox-iso')
        if self.ui.chkParallels.isChecked():
            vmtypes.append('parallels-iso')

        if not vmtypes:
            QtWidgets.QMessageBox.critical(self, "Error", "...Need a virtual machine to be selected...", QtWidgets.QMessageBox.Ok)
            self.vmSelected = False
        else:
            self.vmSelected = True
            if self.ui.chkVagrant.isChecked():
                includeVagrant = True

            if templateFile and isinstance(templateFile, basestring):
                data = self.tPjh.readExistingJsonTemplateFile(templateFile)
                print str(json.dumps(data, ensure_ascii=False, indent=3))
                newJson = {}

                try:
                    newJson['_comment'] = data["_comment"]
                except KeyError, err:
                    #print traceback.format_exc()
                    try:
                        newJson['_comment'] = data['_command']
                    except KeyError:
                        pass

                newJson['variables'] = copy.deepcopy(data['variables'])

                print "."
                print "."
                print "."
                print "."
                for key, value in newJson['variables'].iteritems():
                    print str(key) + " = " + str(value)
                print "."
                print "."
                print "."
                print "."

                self.mergeIfaceVarsWithVarFile()

                for key, value in self.jsonVariables.iteritems():
                    newJson['variables'][key] = value

                newJson['provisioners'] = copy.deepcopy(data['provisioners'])
                newJson['post-processors'] = copy.deepcopy(data['post-processors'])
                newJson['post-processors'][0]['keep_input_artifact'] = True
                newJson['builders'] = []

                #vmtypes = ['vmware-iso', 'virtualbox-iso', 'parallels-iso']
                #includeVagrant = False

                for key, values in data.iteritems():
                    if re.match("builders", key):
                        #print str(values)
                        for item in values:
                            print item['type']
                            if item['type'] in vmtypes:
                                newJson['builders'].append(copy.deepcopy(item))

                    #elif re.match("post-processors", key) and includeVagrant:
                    #    newJson[key] = data[key]

                print str(json.dumps(newJson, ensure_ascii=False, indent=3))
                self.tPjh.saveJsonTemplateFile(filename, newJson)
                self.libc.sync()
                time.sleep(1)
                self.libc.sync()
                time.sleep(1)
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "...Need a valid template file name...", QtWidgets.QMessageBox.Ok)

    def saveVarsToJsonFile(self, filename=""):
        '''
        Save interface values to a json file.

        @param: filename - name of the JSON file

        @author: Roy Nielsen
        '''
        ##############################################
        # stacked widget[0] - general info
        _comment = self.ui.leComment.text().strip()
        vm_name = self.ui.leVmName.text().strip()
        if _comment:
            self.jsonVariables["_comment"] = _comment
        if vm_name:
            self.jsonVariables["vm_name"] = vm_name

        #####
        # Get checkbox values
        self.jsonVariables["desktop"] = str(self.ui.chkDesktop.isChecked()).lower()
        self.jsonVariables["update"] = str(self.ui.chkUpdate.isChecked()).lower()

        ##############################################
        # stacked widget[1] - general info
        iso_path = self.ui.leIsoPath.text().strip()
        if iso_path:
            self.jsonVariables["iso_path"] = iso_path

        ##############################################
        # stacked widget[2] - general info
        cpus = self.ui.leCpus.text().strip()
        memory = self.ui.leMemSize.text().strip()
        disk_size = self.ui.leDiskSize.text().strip()
        if cpus:
            self.jsonVariables["cpus"] = cpus
        if memory:
            self.jsonVariables["memory"] = memory
        if disk_size:
            self.jsonVariables["disk_size"] = disk_size
            
        ##############################################
        # stacked widget[3] - user info
        ssh_user = self.ui.leUserName.text().strip()
        ssh_password = self.ui.leUserPassword.text().strip()
        ssh_verify_password = self.ui.leVerifyPassword.text().strip()
        if ssh_user:
            self.jsonVariables["ssh_username"] = ssh_user
        if ssh_password == ssh_verify_password:
            self.jsonVariables["ssh_password"] = ssh_password
        else:
            self.clearJsonVariables()
            QtWidgets.QMessageBox.critical(self, "Error", "...Password mis-match, please re-enter passwords...", QtWidgets.QMessageBox.Ok)
            self.logger.log(lp.DEBUG, "JSON data: " + str(self.jsonVariables))

        ##############################################
        # stacked widget[4] - proxies
        http_proxy = self.ui.leHttpProxy.text().strip()
        https_proxy = self.ui.leHttpsProxy.text().strip()
        ftp_proxy = self.ui.leFtpProxy.text().strip()
        rsync_proxy = self.ui.leRsyncProxy.text().strip()
        no_proxy = self.ui.leNoProxy.text().strip()
        if http_proxy:
            self.jsonVariables["http_proxy"] = http_proxy
        if https_proxy:
            self.jsonVariables["https_proxy"] = http_proxy
        if ftp_proxy:
            self.jsonVariables["ftp_proxy"] = http_proxy
        if rsync_proxy:
            self.jsonVariables["rsync_proxy"] = http_proxy
        if no_proxy:
            self.jsonVariables["no_proxy"] = http_proxy
        
        self.pjh.saveJsonVarFile(filename, self.jsonVariables)

    def processVm(self):
        '''

        @author: Roy Nielsen
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Processing VM...", QtWidgets.QMessageBox.Ok)

        #####
        # Save temp template file
        templateFileFullPath = self.conf.getCurrentTemplateFilePath()
        partial_prefix = templateFileFullPath.split("/")[-1]
        prefix = ".".join(partial_prefix.split('.')[:-1])
        tmpTemplateFile = tempfile.mkstemp(".json", prefix)[1]
        self.saveTemporaryTemplateFile(tmpTemplateFile)
        self.logger.log(lp.DEBUG, "tmpTemplateFile: " + str(tmpTemplateFile))
        '''
        #####
        # Save temp variables file
        varFileFullPath = self.conf.getCurrentVarFilePath()
        partial_prefix = varFileFullPath.split("/")[-1]
        prefix = ".".join(partial_prefix.split('.')[:-1])
        tmpVarFile = tempfile.mkstemp(".json", prefix)[1]
        self.saveVarsToJsonFile(tmpVarFile)
        self.logger.log(lp.DEBUG, "varFileJson: " + str(tmpVarFile))
        '''
        #####
        # Detect if only one VM build is called for
        vmware = self.ui.chkVmware.isChecked()
        vbox = self.ui.chkVbox.isChecked()
        parallels = self.ui.chkParallels.isChecked()

        only = False
        if vmware and not vbox and not parallels:
            only = 'vmware-iso'
        elif not vmware and vbox and not parallels:
            only = 'virtualbox-iso'
        elif not vmware and not vbox and parallels:
            only = 'parallels-iso'

        if self.vmSelected:
            oldWorkingDir = os.getcwd()
            newWorkingDir = os.chdir(self.workingDir)
            #####
            # Run packer
            pr = PackerRunner(self.conf)
            if only or self.only:
                pr.runPackerBoxcutter(tmpTemplateFile, vmImage=only)
            else:
                pr.runPackerBoxcutter(tmpTemplateFile)
            os.chdir(oldWorkingDir)

    def saveForLater(self):
        '''
        Pop up a dialog asking for a filename (no path) to save the file.  Will
        save the file to the template directory.
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Saving and Processing VM...", QtWidgets.QMessageBox.Ok)
        #####
        # Save varFile
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '.')
        self.getVarsFromIface()
        self.saveTemporaryTemplateFile(filename)
        templateFile = self.conf.getCurrentTemplateFilePath()
        dotFile = "." + filename.split("/")[-1] + "_templateFile"
        dirPath = os.path.dirname(filename)
        shutil.copy(templateFile, dirPath + "/" + dotFile)

    def loadPreviousFile(self):
        '''
        Load previous file (from template directory)
        '''
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.')
        pjh = PackerJsonHandler(self.logger)
        jsonFile = pjh.readExistingJsonTemplateFile(filename)
        self.loadGuiFromPjh(pjh)
        dotFile = "." + filename.split("/")[-1] + "_templateFile"
        dirPath = os.path.dirname(filename)
        self.conf.setCurrentTemplateFilePath(dirPath + "/" + dotFile)

    def resetToDefault(self):
        '''
        Reset the gui to the default var file found in the comment string
        '''
        #####
        # Acquire current json varfile data and print it.
        self.varFilePath = self.conf.getCurrentVarFilePath()

        self.loadValuesToUI(self.varFilePath)
