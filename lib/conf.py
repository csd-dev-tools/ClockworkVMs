# import standard libraries
import re
import os

# local, program specific library
from .loggers import CyLogger
from .loggers import LogPriority as lp


class Conf(object) :
    """
    Class for holding the configuration variables

    Intended initialization happens in program_options.py.

    @author: Roy Nielsen
    """    
    def __init__(self) :
        self.version = "0.0.0.0"
        self.options = []
        self.logger = CyLogger()
        self.currentRepoPath = "~/"
        psudopath = os.path.abspath(os.path.dirname(__file__))
        partialpath = psudopath.split("/")
        self.appPath = os.path.join("/", "/".join(partialpath[:-1]))
        self.currentVarFilePath = ""
        self.currentTemplateFilePath = ""
        self.onlyVmImage = ""
        self.proxy = ""
        self.httpProxy = ""
        self.httpsProxy = ""
        self.ftpProxy = ""
        self.repoRoot = ""

    def getVersion(self) :
        """
        getter for application version

        format: "run_once.py 1.7.x.x"
        """
        return self.version

    def setVersion(self, version="0.0.0.0") :
        """
        setter for application version

        format: "run_once.py 1.7.x.x"
        """
        self.version = version

    def setLogger(self, logger=False):
        """
        setter for command line options
        """
        self.logger = logger

    def getLogger(self):
        """
        getter for command line options
        """
        return self.logger

    def setEnviron(self, environ=""):
        """
        Setter for the password
        """
        self.environ = environ

    def getEnviron(self):
        """
        Getter for the password
        """
        return self.environ

    def setCurrentRepo(self, repoPath=""):
        """
        Setter for the password
        """
        self.currentRepoPath = repoPath

    def getCurrentRepo(self):
        """
        Getter for the password
        """
        return self.currentRepoPath

    def setCurrentVarFilePath(self, varFilePath):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.currentVarFilePath = varFilePath
    
    def getCurrentVarFilePath(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.currentVarFilePath
    
    def setCurrentTemplateFilePath(self, templateFilePath):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.currentTemplateFilePath = templateFilePath
    
    def getCurrentTemplateFilePath(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.currentTemplateFilePath
    
    def setOnlyVmImage(self, onlyVmImage):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.onlyVmImage = onlyVmImage
    
    def getOnlyVmImage(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.onlyVmImage
    
    def setProxy(self, proxy):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.proxy = proxy
    
    def getProxy(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.proxy

    def setHttpProxy(self, httpProxy):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.httpProxy = httpProxy

    def getHttpProxy(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.httpProxy

    def setHttpsProxy(self, httpsProxy):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.httpsProxy = httpsProxy

    def getHttpsProxy(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.httpsProxy

    def setFtpProxy(self, ftpProxy):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.ftpProxy = ftpProxy

    def getFtpProxy(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.ftpProxy
    
    def setRsyncProxy(self, rsyncProxy):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.rsyncProxy = rsyncProxy

    def getRsyncProxy(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.rsyncProxy
    
    def setNoProxy(self, noProxy):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.noProxy = noProxy

    def getNoProxy(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.noProxy
    
    def setRepoRoot(self, repo):
        '''
        Setter for the full path to the boxcutter repo

        @author: Roy Nielsen
        '''
        self.repoRoot = repo

    def getRepoRoot(self):
        '''
        Getter for the full path to the boxcutter repo

        @author: Roy Nielsen
        '''
        return self.repoRoot
    
    def getVmBuildConf(self) :
        """
        return self...
        """
        return self.appPath + "/vmbuilder.conf"

    def returnConf(self) :
        """
        return self...
        """
        return self

    def printSelf(self) :
        """
        print current Configuration
        """
        print "---==# #==---"
        print "script version:  " + str(self.version)
        print "---==# #==---"

    def loggerSelf(self) :
        """
        log current Configuration via logger function
        """
        self.logger.log(lp.DEBUG, "---==# #==---")
        self.logger.log(lp.DEBUG, "script version:  " + str(self.version))
        self.logger.log(lp.DEBUG, "---==# #==---")
