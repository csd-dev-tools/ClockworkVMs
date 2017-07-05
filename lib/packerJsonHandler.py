#!/usr/bin/python
import re
import json
import traceback
from libHelperFunctions import isSaneFilePath
from loggers import LogPriority as lp

#jfp = open("macos1010.json", "r")
#jstuff = json.load(jfp)
#print str(jstuff)
#jfp.close()

class PackerJsonHandler():
    '''
    Wraps packer (https://www.packer.io/) config writing to
    assist with automated builds.

    @author: Roy Nielsen
    '''
    def __init__(self, logger):
        '''
        Initialization method
        '''
        self.curConf = None
        self.logger = logger

        self.clearData()

    def clearData(self):
        '''
        Clear the data, so none is left over from previous loads
        '''
        self._comment = ''
        self.builders = []
        self.postProcessors = []
        self.provisioners = []
        self.variables = {}

    def readExistingJsonVarfile(self, fname=''):
        '''
        Reads in an existing json variables file and appends it to the 
        self.variables list

        @author: Roy Nielsen
        '''
        if fname:
            try:
                jfp = open(str(fname), 'r')
                jstuff = json.load(jfp)
            except:
                trace = traceback.format_exc()
                self.logger.log(lp.INFO, str(trace))
            else:
                self.variables = jstuff
                print str(jstuff)
                '''
                try:
                    self.logger.log(lp.DEBUG, "jstuff: " + str(jstuff))
                except Exception, err:
                    self.logger.log(lp.WARNING, traceback.format_exc())
                    self.logger.log(lp.WARNING, str(err))
                '''
            finally:
                try:
                    jfp.close()
                except:
                    pass
        return self.variables

    def readExistingJsonTemplateFile(self, fname=''):
        '''
        Reads in an existing json template file and sets the following internal
        variables:

        self.variables
        self.builders
        self.postProcessors
        self._comment
        self.provisioners

        @author: Roy Nielsen
        '''
        jstuff = {}
        if fname:
            try:
                jfp = open(fname, 'r')
                jstuff = json.load(jfp)
            except:
                trace = traceback.format_exc()
                self.logger.log(lp.INFO, str(trace))
            else:
                self.variables = jstuff["variables"]
                self.builders = jstuff["builders"]
                self.postProcessors = jstuff["post-processors"]
                try:
                    self._comment = jstuff["_comment"]
                except KeyError, err:
                    self.logger.log(lp.DEBUG, "KeyError: " + traceback.format_exc())
                    try:
                        self._comment = jstuff['_command']
                    except KeyError:
                        pass
                self.provisioners = jstuff["provisioners"]
            finally:
                try:
                    jfp.close()
                except:
                    pass
        return jstuff

    def printVariables(self):
        '''
        Print the currently loaded json "variables"
        '''
        print str(self.variables)

    def printBuilders(self):
        '''
        Print the currently loaded json "builders"
        '''
        print str(self.builders)

    def printPostProcessors(self):
        '''
        Print the currently loaded json "post-processors"
        '''
        print str(self.postProcessors)

    def printComment(self):
        '''
        Print the currently loaded json "_comment"
        '''
        print str(self._comment)

    def printProvisioners(self):
        '''
        Print the currently loaded json "provisioners"
        '''
        print str(self.provisioners)

    def setHdSizeMsizeAndSourceImage(self, hdSize="8000", Msize="4096", sourceImage=None):
        '''
        Set configurable items in the JSON
        '''
        if self.variables:
            self.variables['disk_size'] = hdSize
            self.variables['memory'] = Msize
            self.variables['iso_url'] = sourceImage
        else:
            raise Exception        

    def getComment(self):
        '''
        
        @author: Roy Nielsen
        '''
        try:
            return self.variables['_comment']
        except KeyError:
            return ""

    def getVmName(self):
        '''
        Getter for the vm name

        @author: Roy Nielsen
        '''
        try:
            return self.variables['vm_name']
        except KeyError:
            return ""

    def getCpus(self):
        '''
        Getter for the number of cpus

        @author: Roy Nielsen
        '''
        try:
            return self.variables['cpus']
        except KeyError:
            return ""

    def getMemSize(self):
        '''
        Getter for the size of memory

        @author: Roy Nielsen
        '''
        try:
            return self.variables['memory']
        except KeyError:
            return ""

    def getDiskSize(self):
        '''
        Getter for the disk size

        @author: Roy Nielsen
        '''
        try:
            return self.variables['disk_size']
        except KeyError:
            return ""

    def getDesktop(self):
        '''
        Getter to see if this is a desktop build or not (true/false) - note
        they are not capitalized.

        @author: Roy Nielsen
        '''
        try:
            return self.variables['desktop']
        except KeyError:
            return ""

    def getHeadless(self):
        '''
        Getter to see if this is a headless install or not (true/false) - note
        they are not capitalized.

        @author: Roy Nielsen
        '''
        try:
            return self.variables['headless']
        except KeyError:
            return ""

    def getUpdate(self):
        '''
        Getter to see if updates should be done or not (true/false) - note
        they are not capitalized.

        @author: Roy Nielsen
        '''
        try:
            return self.variables['update']
        except KeyError:
            return ""

    def getCustomScript(self):
        '''
        Getter for the relative path to a custom script to run

        @author: Roy Nielsen
        '''
        try:
            return self.variables['custom-script']
        except KeyError:
            return ""

    def getKickstart(self):
        '''
        Getter for the name of a kickstart file

        @author: Roy Nielsen
        '''
        try:
            return self.variables['kickstart']
        except KeyError:
            return ""

    def getSshUser(self):
        '''
        Getter for the ssh user name

        @author: Roy Nielsen
        '''
        try:
            return self.variables['ssh_username']
        except KeyError:
            return ""

    def getSshPassword(self):
        '''
        Getter for the ssh password

        @author: Roy Nielsen
        '''
        try:
            return self.variables['ssh_password']
        except KeyError:
            return ""

    def getSshUserComment(self):
        '''
        Getter for the ssh user comment/long name

        @author: Roy Nielsen
        '''
        try:
            return self.variables['ssh_user_comment']
        except KeyError:
            return ""

    def getSshUserHomeDir(self):
        '''
        Getter for the ssh user home

        @author: Roy Nielsen
        '''
        try:
            return self.variables['ssh_user_home']
        except KeyError:
            return ""

    def getSshUserShell(self):
        '''
        Getter for the ssh user shell

        @author: Roy Nielsen
        '''
        try:
            return self.variables['ssh_user_shell']
        except KeyError:
            return ""

    def getVmVersion(self):
        '''
        Getter for the virtual machine number

        @author: Roy Nielsen
        '''
        try:
            return self.variables['version']
        except KeyError:
            return ""

    # ---

    def getIsoName(self):
        '''
        Getter for the name of the iso to use as a reference

        @author: Roy Nielsen
        '''
        try:
            return self.variables['iso_name']
        except KeyError:
            return ""

    def getIsoPath(self):
        '''
        Getter for the local path to the iso

        @author: Roy Nielsen
        '''
        try:
            return self.variables['iso_path']
        except KeyError:
            return ""

    def getIsoUrl(self):
        '''
        Getter for the iso url

        @author: Roy Nielsen
        '''
        try:
            return self.variables['iso_url']
        except KeyError:
            return ""

    def getIsoChecksum(self):
        '''
        Getter for the checksum for the iso

        @author: Roy Nielsen
        '''
        try:
            return self.variables['iso_checksum']
        except KeyError:
            return ""

    def getIsoChecksumType(self):
        '''
        Getter for the iso checksum type

        @author: Roy Nielsen
        '''
        try:
            return self.variables['iso_checksum_type']
        except KeyError:
            return ""

    def getHttpProxy(self):
        '''
        Getter for the HTTP_Proxy
        @author: Roy Nielsen
        '''
        try:
            return self.variables['http_proxy']
        except KeyError:
            return ""

    def getHttpsProxy(self):
        '''
        Getter for the https proxy
        @author: Roy Nielsen
        '''
        try:
            return self.variables['https_proxy']
        except KeyError:
            return ""

    def getFtpProxy(self):
        '''
        Getter for the ftp proxy

        @author: Roy Nielsen
        '''
        try:
            return self.variables['ftp_proxy']
        except KeyError:
            return ""

    def getRsyncProxy(self):
        '''
        Getter for the rsync proxy

        @author: Roy Nielsen
        '''
        try:
            return self.variables['rsync_proxy']
        except KeyError:
            return ""

    def getNoProxy(self):
        '''
        Getter for the no proxy

        @author: Roy Nielsen
        '''
        try:
            return self.variables['no_proxy']
        except KeyError:
            return ""

    def getParallelsType(self):
        '''
        Getter for the parallels guest os type

        @author: Roy Nielsen
        '''
        try:
            return self.variables['parallels_guest_os_type']
        except KeyError:
            return ""

    def getVagrantfileTemplate(self):
        '''
        Getter for the vagrantfile template

        @author: Roy Nielsen
        '''
        try:
            return self.variables['vagrantfile_template']
        except KeyError:
            return ""

    def getVmwareType(self):
        '''
        Getter for the vmware type

        @author: Roy Nielsen
        '''
        try:
            return self.variables['vmware_guest_os_type']
        except KeyError:
            return ""

    def getVirtualboxType(self):
        '''
        Getter for the virtualbox type

        @author: Roy Nielsen
        '''
        try:
            return self.variables['virtualbox_guest_os_type']
        except KeyError:
            return ""

    # ---

    def setComment(self, comment=''):
        '''
        Setter for the comment

        @author: Roy Nielsen
        '''
        if comment:
            self.variables['_comment'] = comment

    def setVmName(self, vmName=''):
        '''
        Setter for the virtual machine name

        @author: Roy Nielsen
        '''
        if vmName:
            self.variables['vm_name'] = vmName

    def setCpus(self, cpus=""):
        '''
        Setter for the number of cpus

        @author: Roy Nielsen
        '''
        if cpus and isinstance(cpus, basestring):
            self.variables['cpus'] = cpus

    def setMemSize(self, memory=""):
        '''
        Setter for the memory size

        @author: Roy Nielsen
        '''
        if memory and isinstance(memory, basestring):
            self.variables['memory'] = memory

    def setDiskSize(self, diskSize=''):
        '''
        Setter for the disk size

        @author: Roy Nielsen
        '''
        if diskSize and isinstance(diskSize, basestring):
            self.variables['disk_size'] = diskSize

    def setHeadless(self, headless=''):
        '''
        Setter for bool determining whether or not the vm is a headless 
        install.  (true/false) - not no caps...

        @author: Roy Nielsen
        '''
        if headless and isinstance(headless, basestring):
            self.variables['headless'] = headless

    def setUpdate(self, update=''):
        '''
        Setter for bool determining whether or not to run updates during the 
        vm install.  (true/false) - not no caps...

        @author: Roy Nielsen
        '''
        if update:
            self.variables['update'] = update

    def setCustomScript(self, customScript=''):
        '''
        Setter for the custom script to run

        @author: Roy Nielsen
        '''
        if customScript and isinstance(customScript, basestring):
            self.variables['custom-script'] = customScript

    def setKickstart(self, kickstart=''):
        '''
        Setter for the name of the kickstart file

        @author: Roy Nielsen
        '''
        if kickstart and isinstance(kickstart, basestring):
            self.variables['kickstart'] = kickstart

    def setSshUser(self, sshUser):
        '''
        Setter for the ssh user

        @author: Roy Nielsen
        '''
        if sshUser and isinstance(sshUser, basestring):
            self.variables['ssh-user'] = sshUser

    def setSshPassword(self, sshPassword=""):
        '''
        Setter for the ssh user's password

        @author: Roy Nielsen
        '''
        if sshPassword and isinstance(sshPassword, basestring):
            self.variables['ssh-password'] = sshPassword

    def setSshUserComment(self, userComment=''):
        '''
        Getter for the ssh user comment/long name

        @author: Roy Nielsen
        '''
        if userComment and isinstance(userComment, basestring):
            self.variables['ssh_user_comment'] = userComment

    def setSshUserHome(self, userHome=''):
        '''
        Getter for the ssh user home

        @author: Roy Nielsen
        '''
        if userHome and isinstance(userHome, basestring):
            self.variables['ssh_user_home'] = userHome

    def setSshUserShell(self, userShell=''):
        '''
        Getter for the ssh user shell

        @author: Roy Nielsen
        '''
        if userShell and isinstance(userShell, basestring):
            self.variables['ssh_user_shell'] = userShell

    def setVmVersion(self, vmVersion=''):
        '''
        Setter for the version for the virtual machine

        @author: Roy Nielsen
        '''
        if vmVersion and isinstance(vmVersion, basestring):
            self.variables['version'] - vmVersion

    # ---

    def setIsoName(self, isoName=""):
        '''
        Setter for the iso name

        @author: Roy Nielsen
        '''
        if isoName and isinstance(isoName, basestring):
            self.variables["iso"] = isoName

    def setIsoPath(self, isoPath=""):
        '''
        Setter for the iso path

        @author: Roy Nielsen
        '''
        if isoPath and isinstance(isoPath, basestring):
            self.variables["iso-path"] = isoPath

    def setIsoUrl(self, isoUrl=""):
        '''
        Setter for the iso url

        @author: Roy Nielsen
        '''
        if isoUrl and isinstance(isoUrl, basestring):
            self.variables["iso-url"] = isoUrl

    def setIsoChecksum(self, isoChecksum=""):
        '''
        Setter for the iso checksum

        @author: Roy Nielsen
        '''
        if isoChecksum and isinstance(isoChecksum, basestring):
            self.variables["iso-checksum"] = isoChecksum

    def setIsoChecksumType(self, isoChecksumType=""):
        '''
        Setter for the iso checksum type

        @author: Roy Nielsen
        '''
        if isoChecksumType and isinstance(isoChecksumType, basestring):
            self.variables["iso"] = isoChecksumType

    def setHttpProxy(self, httpProxy=''):
        '''
        Setter for the http proxy

        @author: Roy Nielsen
        '''
        if httpProxy and isinstance(httpProxy, basestring):
            self.variables["httpProxy"] = httpProxy

    def setHttpsProxy(self, httpsProxy=''):
        '''
        Setter for the https proxy

        @author: Roy Nielsen
        '''
        if httpsProxy and isinstance(httpsProxy, basestring):
            self.variables["httpsProxy"] = httpsProxy

    def setFtpProxy(self, ftpProxy=''):
        '''
        Setter for the ftp proxy

        @author: Roy Nielsen
        '''
        if ftpProxy and isinstance(ftpProxy, basestring):
            self.variables["ftpProxy"] = ftpProxy

    def setRsyncProxy(self, rsyncProxy=''):
        '''
        Setter for the rsync proxy

        @author: Roy Nielsen
        '''
        if rsyncProxy and isinstance(rsyncProxy, basestring):
            self.variables["rsyncProxy"] = rsyncProxy

    def setNoProxy(self, noProxy=''):
        '''
        Setter for the no proxy

        @author: Roy Nielsen
        '''
        if noProxy and isinstance(noProxy, basestring):
            self.variables["no_proxy"] = noProxy

    def setParallelsType(self, parallelsType=''):
        '''
        Setter for the parallels type

        @author: Roy Nielsen
        '''
        if parallelsType and isinstance(parallelsType, basestring):
            self.variables['parallels_guest_os_type'] = parallelsType

    def setVagrantfileTemplate(self, vagrantfileTemplate=''):
        '''
        Setter for the vagrat type

        @author: Roy Nielsen
        '''
        if vagrantfileTemplate and isinstance(vagrantfileTemplate, basestring):
            self.variables['vagrantfile_template'] = vagrantfileTemplate

    def setVmwareType(self, vmwareType=''):
        '''
        Setter for the vmware type

        @author: Roy Nielsen
        '''
        if vmwareType and isinstance(vmwareType, basestring):
            self.variables['vmware_guest_os_type'] = vmwareType

    def setVirtualboxType(self, virtualboxType=''):
        '''
        Setter for the virtualbox type

        @author: Roy Nielsen
        '''
        if virtualboxType and isinstance(virtualboxType, basestring):
            self.variables['virtualbox_guest_os_type'] = virtualboxType

    def saveJsonVarFile(self, fname="", data=None):
        '''
        Save a boxcutter varfile

        @author: Roy Nielsen
        '''
        self.logger.log(lp.DEBUG, "fname: " + str(fname))
        self.logger.log(lp.DEBUG, "jsonData: " + str(data))
        if fname and isSaneFilePath(fname):
            with open(fname, 'w') as outfile:
                if data:
                    outfile.write(json.dumps(data, ensure_ascii=False, indent=3))
                else:
                    outfile.write(json.dumps(self.variables, ensure_ascii=False, indent=3))

    def saveJsonTemplateFile(self, fname="", data=None):
        '''
        Save a boxcutter template file.

        @author: Roy Nielsen
        '''
        if not data or not isinstance(data, dict):
            data = {}
            data['variables'] = self.variables
            data['builders'] = self.builders
            data['post-processors'] = self.postProcessors
            data['provisioners'] = self.provisioners
            data['_comment'] = self._comment
        else:
            print str(json.dumps(data, ensure_ascii=False, indent=3))

        cleanData = self.cleanUserVars(data)
        with open(fname, 'w') as outfile:
            outfile.write(json.dumps(cleanData, ensure_ascii=False, indent=3))

    def cleanUserVars(self, data={}):
        '''
        '''
        self.logger.log(lp.DEBUG, str(data['variables']))
        for key, value in data['variables'].iteritems():
            data['variables'][key] = self.sanitizeString(value, key)
        self.logger.log(lp.DEBUG, "---")
        self.logger.log(lp.DEBUG, str(data['variables']))

        self.logger.log(lp.DEBUG, "-----")
        self.logger.log(lp.DEBUG, str(data['provisioners']))
        x = 0
        for item in data['provisioners']:
            for key, value in item.iteritems():
                
                if isinstance(value, basestring):
                    data['provisioners'][x][key] = self.sanitizeString(value, key)
                if isinstance(value, list):
                    y = 0
                    for atom in value:
                        data['provisioners'][x][key][y] = self.sanitizeString(atom)
                        y = y + 1
            x = x + 1
        self.logger.log(lp.DEBUG, "---")
        self.logger.log(lp.DEBUG, str(data['provisioners']))

        self.logger.log(lp.DEBUG, "-----")
        self.logger.log(lp.DEBUG, str(data['builders']))

        return data
    
    def sanitizeString(self, string="", checkKey=""):
        '''
        '''
        returnValue = string
        if string and isinstance(string, basestring):
            if checkKey and isinstance(checkKey, basestring):
                if re.search("proxy", checkKey, re.IGNORECASE) or \
                   re.search("ssh_user", checkKey, re.IGNORECASE) or \
                   re.search("ssh_password", checkKey, re.IGNORECASE): # or \
                    # re.search("{{user `", string) or re.search("{{env `", string):
                    returnValue = re.sub("{{user", "{{ user", returnValue)
                    returnValue = re.sub("{{env", "{{ env", returnValue)
                    returnValue = re.sub("`}}", "` }}", returnValue)
            else:
                if re.search("proxy", string, re.IGNORECASE) or \
                   re.search("ssh_user", string, re.IGNORECASE) or \
                   re.search("ssh_password", string, re.IGNORECASE): # or\
                    # re.search("{{user `", string) or re.search("{{env `", string):
                    returnValue = re.sub("{{user", "{{ user", returnValue)
                    returnValue = re.sub("{{env", "{{ env", returnValue)
                    returnValue = re.sub("`}}", "` }}", returnValue)

        return returnValue
