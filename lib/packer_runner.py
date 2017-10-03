import os
import re
import traceback

from run_commands import RunWith
from loggers import LogPriority as lp

class MissingParameterError(Exception):
    """
    Meant to be thrown if a required parameter is missing.

    @author: Roy Nielsen
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class PackerRunner(object):
    """
    """
    def __init__(self, conf):
        """
        """
        self.conf = conf
        self.logger = self.conf.getLogger()
        self.rw = RunWith(self.logger)

    def runPackerBoxcutter(self, templateFile="", varFile="", vmImage=""):
        """
        Run packer on a boxcutter repo

        @param: templateFile - Name of the packer template to process
        @param: varFile - Name of optional variables file
        @param: vmImage - Will create only this type of image, one of:
                          parallels-iso - Parallels desktop virtualization (requires the Pro Edition - Desktop edition won't work)
                          virtualbox-iso - VirtualBox desktop virtualization
                          vmware-iso - VMware Fusion or VMware Workstation desktop virtualization

        examples:

            templateFile = "ubuntu.json"
            varFile = "ubuntu1604.json"
            vmImage = "vmware-iso"

        """

        self.logger.log(lp.DEBUG, "templateFile: " + str(templateFile))
        self.logger.log(lp.DEBUG, "varFile: " + str(varFile))
        self.logger.log(lp.DEBUG, "vmImage: " + str(vmImage))

        returnDir = os.getcwd()
        os.chdir(self.conf.getCurrentRepo())
        
        
        cmd = ["/usr/local/bin/packer", "build"]
        
        #####
        # Get and set the proxy if there is one
        shellEnviron = os.environ.copy()
        self.logger.log(lp.DEBUG, "Env: " + str(shellEnviron))
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
            shellEnviron['HTTP_PROXY'] = proxy
            shellEnviron['HTTPS_PROXY'] = proxy
            shellEnviron['FTP_PROXY'] = proxy
            shellEnviron['RSYNC_PROXY'] = proxy
        if httpProxy and isinstance(httpProxy, basestring):
            shellEnviron['http_proxy'] = httpProxy
            shellEnviron['HTTP_PROXY'] = httpProxy
        if httpsProxy and isinstance(httpsProxy, basestring):
            shellEnviron['https_proxy'] = httpsProxy
            shellEnviron['HTTPS_PROXY'] = httpsProxy
        if ftpProxy and isinstance(ftpProxy, basestring):
            shellEnviron['ftp_proxy'] = ftpProxy
            shellEnviron['FTP_PROXY'] = ftpProxy
        if rsyncProxy and isinstance(rsyncProxy, basestring):
            shellEnviron['rsync_proxy'] = rsyncProxy
            shellEnviron['RSYNC_PROXY'] = rsyncProxy
        if noProxy and isinstance(noProxy, basestring):
            shellEnviron['no_proxy'] = noProxy
            shellEnviron['NO_PROXY'] = noProxy

        self.logger.log(lp.DEBUG, "Env With Proxies: " + str(shellEnviron))

        #####
        # Add specific VM if requested
        if vmImage and isinstance(vmImage, basestring):
            cmd.append("-only=" + vmImage)

        #####
        # Add the varFile
        if varFile and isinstance(varFile, basestring):
            cmd.append("-var-file=" + str(varFile))

        self.logger.log(lp.DEBUG, "CMD so far: " + str(cmd))
        self.logger.log(lp.DEBUG, "templateFile: " + str(templateFile))

        if not templateFile or not isinstance(templateFile, basestring):
            raise MissingParameterError("Parameter required.")
        elif re.match("^win", varFile):
            #####
            # Windows repos don't seem to have both varFile and templateFile...
            pass
        else:
            cmd.append(str(templateFile))

        self.logger.log(lp.DEBUG, "CMD to run: " + str(cmd))

        self.rw.setCommand(cmd, env=shellEnviron)

        self.rw.waitNpassThruStdout()

        os.chdir(returnDir)
