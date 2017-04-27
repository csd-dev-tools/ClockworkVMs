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

from lib.libHelperFunctions import isSaneFilePath

#####
# Import pyuic5 compiled PyQt ui files
from ui.ConfigureRepoFilesystemLocations_ui import Ui_Dialog


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


class ConfigureRepoFilesystemLocations(QtWidgets.QDialog):
    """
    Class to manage the set password dialog...

    @author: Roy Nielsen
    """
    def __init__(self, conf, parent=None):
        """
        Initialization method...

        @author: Roy Nielsen
        """
        super(ConfigureRepoFilesystemLocations, self).__init__(parent)

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
