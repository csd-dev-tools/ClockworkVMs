###############################################################################
#                                                                             #
# Copyright 2015.  Los Alamos National Security, LLC. This material was       #
# produced under U.S. Government contract DE-AC52-06NA25396 for Los Alamos    #
# National Laboratory (LANL), which is operated by Los Alamos National        #
# Security, LLC for the U.S. Department of Energy. The U.S. Government has    #
# rights to use, reproduce, and distribute this software.  NEITHER THE        #
# GOVERNMENT NOR LOS ALAMOS NATIONAL SECURITY, LLC MAKES ANY WARRANTY,        #
# EXPRESS OR IMPLIED, OR ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  #
# If software is modified to produce derivative works, such modified software #
# should be clearly marked, so as not to confuse it with the version          #
# available from LANL.                                                        #
#                                                                             #
# Additionally, this program is free software; you can redistribute it and/or #
# modify it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 2 of the License, or (at your  #
# option) any later version. Accordingly, this program is distributed in the  #
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the     #
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    #
# See the GNU General Public License for more details.                        #
#                                                                             #
###############################################################################

# ============================================================================ #
#               Filename          $RCSfile: admin_creds.py,v $
#               Description       Class to handle GUI for authentication of an
#                                 admin user, with the purpose of running stonix 
#                                 as that admin user.  User may be different 
#                                 from the user that is launching the class.
#               OS                Mac OS X
#               Author            Roy Nielsen
#               Last updated by   $Author: $
#               Notes             
#               Release           $Revision: 1.0 $
#               Modified Date     $Date:  $
# ============================================================================ #

import os
import re
import pwd
import sys
import time
import getpass
import tempfile
from subprocess import Popen, PIPE, STDOUT

#####
# PyQt libraries
from PyQt5 import QtCore, QtGui, QtWidgets

##########
# local app libraries
from admin_credentials_ui import Ui_AdministratorCredentials

from lib.run_commands import RunWith, RunThread, runMyThreadCommand
from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp
from lib.manage_user.manage_user import ManageUser

class AdministratorCredentials(QtWidgets.QDialog) :
    """
    Class to manage the dialog to get the property number
    
    @author: Roy Nielsen
    """
    
    creds = QtCore.pyqtSignal('QString', 'QString')
    
    def __init__(self, conf, parent=None) :
        """
        Initialization method
        
        @author: Roy Nielsen
        """
        super(AdministratorCredentials, self).__init__(parent)
        
        self.ui = Ui_AdministratorCredentials()
        self.ui.setupUi(self)
        self.conf = conf
        
        self.logger = self.conf.getLogger()
        self.mu = ManageUser(logger=self.logger)
        self.rw = RunWith(self.logger)

        self.username = ""
        self.password = ""
        self.cmd = ""
        self.tmpDir = ""

        #####
        # Set up signals and slots
        self.ui.authUserButton.clicked.connect(self.isPassValid)
        self.ui.cancelButton.clicked.connect(self.rejectApp)

        self.logger.log(lp.DEBUG, "Finished initializing AdministratorCredentials Class...")

    def rejectApp(self) :
        """
        Reject slot, print a message before sending the reject signal...
        
        Author: Roy Nielsen
        """
        QtWidgets.QMessageBox.warning(self, "Warning", "You hit Cancel, exiting program.", QtWidgets.QMessageBox.Ok)
        QtCore.QCoreApplication.instance().quit()

    def isPassValid(self) :
        """
        Set the admin username and password values of the class.
        
        Author: Roy Nielsen
        """
        self.logger.log(lp.DEBUG, "Entering isPassValid in admin_creds...")
        #####
        # Grab the QString out of the QLineEdit field
        myuser = self.ui.adminName.text()

        #####
        # Convert myuser into a string
        self.username = "%s" % myuser

        #####
        # Grab the QString out of the QLineEdit field
        mypass = self.ui.passwordLineEdit.text()
        
        #####
        # Convert mypass into a string
        self.password = "%s" % mypass
        
        result = self.mu.authenticate(self.username, self.password)
        self.logger.log(lp.DEBUG, str(self.username) + " is an admin...")
    
        if result :
            self.logger.log(lp.DEBUG, "Authentication success...")
            self.creds.emit(self.username, self.password)
            self.accept()
        else :
            #####
            # User is an admin, report invalid password and try again...
            self.logger.log(lp.DEBUG, "Authentication test FAILURE...")
            QtWidgets.QMessageBox.warning(self, "Warning", "...Incorrect Password, please try again.", QtWidgets.QMessageBox.Ok)
        self.logger.log(lp.DEBUG, "Finished isPassValid...")
