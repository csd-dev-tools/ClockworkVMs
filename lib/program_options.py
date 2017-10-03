###############################################################################
#                                                                             #
# Copyright, 2008, Los Alamos National Security, LLC.                         #
#                                                                             #
# This software was produced under a U.S. Government contract by Los Alamos   #
# National Laboratory, which is operated by Los Alamos National Security,     #
# LLC., under Contract No. DE-AC52-06NA25396 with the U.S. Department of      #
# Energy.                                                                     #
#                                                                             #
# The U.S. Government is licensed to use, reproduce, and distribute this      #
# software. Permission is granted to the public to copy and use this software #
# without charge, provided that this Notice and any statement of authorship   #
# are reproduced on all copies.                                               #
#                                                                             #
# Neither the Government nor the Los Alamos National Security, LLC., makes    #
# any warranty, express or implied, or assumes any liability or               #
# responsibility for the use of this software.                                #
#                                                                             #
###############################################################################
from __future__ import absolute_import

#####
# python standard libraries
import re
import os
from optparse import OptionParser, SUPPRESS_HELP

#####
# PNpass libraries
from .conf import Conf
from .loggers import CyLogger
from .loggers import LogPriority as lp
from .libHelperFunctions import get_console_user
from .libMacOSHelperFunctions import getResourcesDir

#####
# Stonix libraries
from .environment import Environment
from logging import root


class ProgramOptions(object) :
    """
    Class for holding the command line options
    """
    def __init__(self):
        """
        Initialization routine for our program options

        Acquiring command line arguments with OptionParser
        """
        self.version = ""
        self.environ = Environment()

        #####
        # Define the default log directory, and make sure it
        # it exists as a directory.
        self.resources = getResourcesDir()
        defaultLogDir = os.path.join(self.resources, "logs")
        """
        if not os.path.isdir(defaultLogDir):
            if os.path.exists(defaultLogDir):
                os.unlink(defaultLogDir)
            os.mkdir(defaultLogDir)
        """
        #####
        # Collect the passed in parameters, or define them as default.

        parser = OptionParser(usage="  %prog [options]\n\n"  + \
             "Only options are to change the logging level of the application.", \
             version="%prog 0.7.0.25")

        #####
        # Logging level lp.VERBOSE
        parser.add_option("-v", "--verbose", action="store_true", \
                          dest="verbose", default=False, \
                          help="Print status messages")

        #####
        # Logging level lp.DEBUG
        parser.add_option("-d", "--debug", action="store_true", dest="debug", \
                          default=False, help="Print debug messages")

        #####
        # Where to put the logs.
        parser.add_option("-l", "--log-path", action="store", dest="logPath", \
                          default="/tmp/", help="Path to put the logs")

        #####
        # General proxy - set all proxy values to this value
        parser.add_option("-p", "--proxy", action="store", dest="proxy", \
                          default="", help="Sets HTTP_PROXY, HTTPS_PROXY and FTP_PROXY to the value passed in.")

        #####
        # To set the HTTP_PROXY setting
        parser.add_option("--http-proxy", action="store", dest="httpProxy", \
                          default="", help="Sets the http_proxy.")

        #####
        # To set the HTTPS_PROXY setting
        parser.add_option("--https-proxy", action="store", dest="httpsProxy", \
                          default="", help="Sets the https_proxy.")

        #####
        # To set the FTP_PROXY setting
        parser.add_option("--ftp-proxy", action="store", dest="ftpProxy", \
                          default="", help="Sets the ftp_proxy.")

        #####
        # To set the RSYNC_PROXY setting
        parser.add_option("--rsync-proxy", action="store", dest="rsyncProxy", \
                          default="", help="Sets the rsync_proxy.")

        #####
        # To set the NO_PROXY setting
        parser.add_option("--no-proxy", action="store", dest="noProxy", \
                          default="", help="Sets the no_proxy.")

        #####
        # Where to put the logs.
        parser.add_option("--repo-root", action="store", dest="repoRoot", \
                          default="/opt/tools/src/boxcutter", help="Path to put the logs")

        (self.options, self.args) = parser.parse_args()

        programVersion = parser.get_version()
        programVersion = programVersion.split(' ')
        self.version = programVersion[1]

        if self.getDebugMode():
            loglevel = lp.DEBUG
        elif self.getVerboseMode():
            loglevel = lp.VERBOSE
        else:
            loglevel = lp.WARNING

        # self.logger = CyLogger(level=loglevel)
        self.logger = CyLogger(debug_mode=lp.DEBUG)

        #####
        # Instanciate a configuration object and initialize its
        # variables.  This object is what will be passed to all
        # of the objects in this program for shared knowledge,
        # much like the Environment in Stonix.
        self.conf = Conf()
        #programLogDir = self.get_log_path()
        self.logger.initializeLogs(logdir=self.options.logPath)
        self.conf.setLogger(self.logger)

        self.conf.setVersion(self.getVersion())
        self.conf.setEnviron(self.getEnviron())

        self.conf.setHttpProxy(self.getHttpProxy())
        self.conf.setHttpsProxy(self.getHttpsProxy())
        self.conf.setFtpProxy(self.getFtpProxy())
        self.conf.setRsyncProxy(self.getRsyncProxy())
        self.conf.setNoProxy(self.getNoProxy())

        if self.options.proxy and isinstance(self.options.proxy, basestring):
            #####
            # Need better input validation...
            self.conf.setHttpProxy(self.getProxy())
            self.conf.setHttpsProxy(self.getProxy())
            self.conf.setFtpProxy(self.getProxy())
            self.conf.setProxy(self.getProxy())

        self.conf.setRepoRoot(self.getRepoRoot())

    def getDebugMode(self):
        """
        Return the debug flag
        """
        return self.options.debug

    def getVerboseMode(self):
        """
        Return the debug flag
        """
        return self.options.verbose

    def getEnviron(self):
        """
        Return the environment object
        """
        return self.environ

    def getVersion(self) :
        """
        Return the version of this application
        """
        return self.version

    def getLogPath(self):
        """
        Return the command line option stored in self.options.logPath
        """
        return self.options.logPath

    def returnConf(self):
        """
        Return a "Conf" class with valid configuration information..
        """
        return self.conf

    def getHttpProxy(self):
        """
        Return the http proxy value found in the 'self.options'
        """
        return self.options.httpProxy

    def getHttpsProxy(self):
        """
        Return the https proxy value found in the 'self.options'
        """
        return self.options.httpsProxy

    def getFtpProxy(self):
        """
        Return the ftp proxy value found in the 'self.options'
        """
        return self.options.ftpProxy

    def getRsyncProxy(self):
        """
        Return the ftp proxy value found in the 'self.options'
        """
        return self.options.rsyncProxy

    def getNoProxy(self):
        """
        Return the ftp proxy value found in the 'self.options'
        """
        return self.options.noProxy

    def getProxy(self):
        """
        Return the http proxy value found in the 'self.options'
        """
        return self.options.proxy

    def getRepoRoot(self):
        """
        Return the boxcutter repo root
        """
        return self.options.repoRoot
