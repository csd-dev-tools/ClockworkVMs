#!/usr/bin/python

import os
import re
import sys
import getpass
import traceback
import subprocess

from lib.run_commands import RunWith
from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp

user = raw_input("User: " )
userpass = getpass.getpass("Password: ")
#print userpass
subcmd = "/bin/ls -lah /Applications/*"

cmd = ["/usr/bin/osascript", "-e", 'do shell script "{0}" user name "{1}" password "{2}" with administrator privileges'.format(subcmd, user, userpass)]

myout = ''
myerr = ''

try:
    myout, myerr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE, env=None).communicate()
except OSError, err:
    print traceback.format_exc(err)
    print str(err)
else:
    sys.stdout.flush()

print "myout: " + str(myout)
print "\n"
print "myerr: " + str(myerr)


logger = CyLogger(debug_mode=True)
logger.initializeLogs()
rw = RunWith(logger)

cmd = ["/usr/bin/osascript", "-e", '\'do shell script "{0}" user name "{1}" password "{2}" with administrator privileges\''.format(subcmd, user, userpass)]

rw.setCommand(cmd)
rw.waitNpassThruStdout()

for line in rw.getStdout().split("\n"):

    print line + "\n"


