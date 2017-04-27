from __future__ import absolute_import

import os
import re
import sys
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
        self.pjh = PackerJsonHandler(self.logger)
        self.jsonData = {}
        self.vmTypes = []
        self.doVagrantBox = False

        #####
        # Handle button box
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject) 

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.processVm) 

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveForLater) 

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Open).clicked.connect(self.loadPreviousFile) 

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
                self.jsonData = self.pjh.readExistingJsonVarfile(loadfile)
                self.logger.log(lp.DEBUG, "JSON loaded: " + str(self.jsonData))
            except Exception, err:
                QtWidgets.QMessageBox.critical(self, "Error", "...Exception trying to read packer json...", QtWidgets.QMessageBox.Ok)
                raise err
            else:
                #####
                # Fill out labels
                self.ui.leComment.setText(self.pjh.getComment())
                self.ui.leVmName.setText(self.pjh.getVmName())
                self.ui.leCpus.setText(self.pjh.getCpus())
                self.ui.leMemSize.setText(self.pjh.getMemSize())
                self.ui.leDiskSize.setText(self.pjh.getDiskSize())
                self.ui.leUserName.setText(self.pjh.getUser())
                self.ui.leUserPassword.setText(self.pjh.getPassword())
                self.ui.leVerifyPassword.setText(self.pjh.getPassword())
                self.ui.leIsoHash.setText(self.pjh.getIsoChecksum())
                self.ui.leIsoUrl.setText(self.pjh.getIsoUrl())
                if not self.pjh.getIsoPath():
                    varFileDir = os.path.dirname(self.varFilePath)
                    isoPath = varFileDir + "/Downloads/"
                    if not os.path.exists(isoPath):
                        os.mkdir(isoPath)
                    elif not os.path.isdir(isoPath):
                        #####
                        # Move/delete what's there
                        pass
                    self.ui.leIsoPath.setText(isoPath)
                    self.pjh.setIsoPath(isoPath)
                else:
                    self.ui.leIsoPath.setText(self.pjh.getIsoPath())

                #####
                # Turn of checkbox tri-state
                self.ui.chkDesktop.setTristate(False)
                self.ui.chkUpdate.setTristate(False)
                self.ui.chkVmware.setTristate(False)
                self.ui.chkVbox.setTristate(False)
                self.ui.chkParallels.setTristate(False)
                self.ui.chkVagrant.setTristate(False)
                
                #####
                # Fill out desktop and updates
                if re.match("false", self.pjh.getDesktop()):
                    self.ui.chkDesktop.setChecked(False)
                else:
                    self.ui.chkDesktop.setChecked(True)

                if re.match("false", self.pjh.getUpdate()):
                    self.ui.chkUpdate.setChecked(False)
                else:
                    self.ui.chkUpdate.setChecked(True)
                
                #####
                # Set image boxes to checked, and read only...
                self.ui.chkVmware.setChecked(False)
                self.ui.chkVbox.setChecked(False)
                self.ui.chkParallels.setChecked(False)
                self.ui.chkVagrant.setChecked(False)
                """
                self.ui.chkVmware.setCheckable(False)
                self.ui.chkVbox.setCheckable(False)
                self.ui.chkParallels.setCheckable(False)
                self.ui.chkVagrant.setCheckable(False)
                """
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "...Bad path for packer json...", QtWidgets.QMessageBox.Ok)
            self.close()

    def getVarsFromIface(self):
        '''
        '''
        #####
        # Acquire data from UI
        _comment = self.ui.leComment.text().strip()
        vm_name = self.ui.leVmName.text().strip()
        cpus = self.ui.leCpus.text().strip()
        memory = self.ui.leMemSize.text().strip()
        disk_size = self.ui.leDiskSize.text().strip()
        iso_path = self.ui.leIsoPath.text().strip()
        ssh_user = self.ui.leUserName.text().strip()
        ssh_password = self.ui.leUserPassword.text().strip()
        ssh_verify_password = self.ui.leVerifyPassword.text().strip()


        #####
        # Insert the valid values into the self.jsonData
        if _comment:
            self.jsonData["_comment"] = _comment
        if vm_name:
            self.jsonData["vm_name"] = vm_name
        if cpus:
            self.jsonData["cpus"] = cpus
        if memory:
            self.jsonData["memory"] = memory
        if disk_size:
            self.jsonData["disk_size"] = disk_size
        if iso_path:
            self.jsonData["iso_path"] = iso_path
        if ssh_user:
            self.jsonData["ssh_username"] = ssh_user
        #####
        # Get checkbox values
        self.jsonData["desktop"] = str(self.ui.chkDesktop.isChecked()).lower()
        self.jsonData["update"] = str(self.ui.chkUpdate.isChecked()).lower()
        if not self.ui.chkVagrant.isChecked:
            self.only = True
        else:
            self.only = False
        if ssh_password and ssh_password == ssh_verify_password:
            self.jsonData["ssh_password"] = ssh_password
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "...Password mis-match, please re-enter passwords...", QtWidgets.QMessageBox.Ok)

        self.logger.log(lp.DEBUG, "JSON data: " + str(self.jsonData))

    def mergeIfaceVarsWithVarFile(self):
        '''
        '''
        loadFile = self.conf.getCurrentVarFilePath()
        self.jsonData = self.pjh.readExistingJsonVarfile(loadFile)
        self.getVarsFromIface()

    def saveTemporaryTemplateFile(self, filename=''):
        '''
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
            
        varsFromIface = {}
        varsFromIface = self.mergeIfaceVarsWithVarFile()

        if not vmtypes:
            QtWidgets.QMessageBox.critical(self, "Error", "...Need a virtual machine to be selected...", QtWidgets.QMessageBox.Ok)
        else:
            if self.ui.chkVagrant.isChecked():
                includeVagrant = True

            if templateFile and isinstance(templateFile, basestring):
                data = self.pjh.readExistingJsonTemplateFile(templateFile)
                print str(json.dumps(data, ensure_ascii=False, indent=3))
                newJson = {}

                try:
                    newJson['_comment'] = data["_comment"]
                except KeyError, err:
                    print traceback.format_exc()
                    try:
                        newJson['_command'] = data['_command']
                    except KeyError:
                        pass

                newJson['variables'] = data['variables']

                self.getVarsFromIface()

                for key, value in self.jsonData.iteritems():
                    newJson['variables'][key] = value

                newJson['provisioners'] = data['provisioners']
                newJson['post-processors'] = data['post-processors']
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
                                newJson['builders'].append(item)

                    #elif re.match("post-processors", key) and includeVagrant:
                    #    newJson[key] = data[key]
                print str(json.dumps(newJson, ensure_ascii=False, indent=3))
                self.pjh.saveJsonTemplateFile(filename, newJson)
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "...Need a valid template file name...", QtWidgets.QMessageBox.Ok)

    def saveVarsToJsonFile(self, filename=""):
        '''
        '''
        _comment = self.ui.leComment.text().strip()
        vm_name = self.ui.leVmName.text().strip()
        cpus = self.ui.leCpus.text().strip()
        memory = self.ui.leMemSize.text().strip()
        disk_size = self.ui.leDiskSize.text().strip()
        iso_path = self.ui.leIsoPath.text().strip()
        ssh_user = self.ui.leUserName.text().strip()
        ssh_password = self.ui.leUserPassword.text().strip()
        ssh_verify_password = self.ui.leVerifyPassword.text().strip()

        if _comment:
            self.jsonData["_comment"] = _comment
        if vm_name:
            self.jsonData["vm_name"] = vm_name
        if cpus:
            self.jsonData["cpus"] = cpus
        if memory:
            self.jsonData["memory"] = memory
        if disk_size:
            self.jsonData["disk_size"] = disk_size
        if iso_path:
            self.jsonData["iso_path"] = iso_path
        if ssh_user:
            self.jsonData["ssh_username"] = ssh_user
        if ssh_password == ssh_verify_password:
            self.jsonData["ssh_password"] = ssh_password

            #####
            # Get checkbox values
            self.jsonData["desktop"] = str(self.ui.chkDesktop.isChecked()).lower()
            self.jsonData["update"] = str(self.ui.chkUpdate.isChecked()).lower()

            self.logger.log(lp.DEBUG, "JSON data: " + str(self.jsonData))

            self.pjh.saveJsonVarFile(filename, self.jsonData)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "...Password mis-match, please re-enter passwords...", QtWidgets.QMessageBox.Ok)

    def processVm(self):
        '''

        @author: Roy Nielsen
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Processing VM...", QtWidgets.QMessageBox.Ok)

        #####
        # Save temp template file
        varFileFullPath = self.conf.getCurrentTemplateFilePath()
        partial_prefix = varFileFullPath.split("/")[-1]
        prefix = ".".join(partial_prefix.split('.')[:-1])
        tmpTemplateFile = tempfile.mkstemp(".json", prefix)[1]
        self.saveTemporaryTemplateFile(tmpTemplateFile)
        self.logger.log(lp.DEBUG, "tmpTemplateFile: " + str(tmpTemplateFile))

        #####
        # Save temp variables file
        varFileFullPath = self.conf.getCurrentVarFilePath()
        partial_prefix = varFileFullPath.split("/")[-1]
        prefix = ".".join(partial_prefix.split('.')[:-1])
        tmpVarFile = tempfile.mkstemp(".json", prefix)[1]
        self.saveVarsToJsonFile(tmpVarFile)
        self.logger.log(lp.DEBUG, "varFileJson: " + str(tmpVarFile))

        #####
        # Run packer
        pr = PackerRunner(self.conf)
        pr.runPackerBoxcutter(tmpTemplateFile)

    def saveForLater(self):
        '''
        Pop up a dialog asking for a filename (no path) to save the file.  Will
        save the file to the template directory.
        '''
        QtWidgets.QMessageBox.information(self, "Information", "...Saving and Processing VM...", QtWidgets.QMessageBox.Ok)
        #####
        # Save varFile
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '.')

        self.saveVarsToJsonFile(filename)

    def loadPreviousFile(self):
        '''
        Load previous file (from template directory)
        '''
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')

        self.loadValuesToUI(filename)

    def resetToDefault(self):
        '''
        Reset the gui to the default var file found in the comment string
        '''
        #####
        # Acquire current json varfile data and print it.
        self.varFilePath = self.conf.getCurrentVarFilePath()

        self.loadValuesToUI(self.varFilePath)
