"""
Helper functions, OS agnostic

@author: Roy Nielsen
"""
from __future__ import absolute_import
#--- Native python libraries
import re
import os
import sys
import time
import ctypes
import traceback
from subprocess import Popen, STDOUT, PIPE
try:
    import termios
except:
    pass

#--- non-native python libraries in this source tree
from . loggers import CyLogger
from . loggers import LogPriority as lp
from . run_commands import RunWith

logger = CyLogger()
run = RunWith(logger)

###########################################################################

def getConsoleUser():
    """
    Get the user that owns the console on the Mac.  This user is the user that
    is logged in to the GUI.
    """
    user = False

    cmd = ["/usr/bin/stat", "-f", "'%Su'", "/dev/console"]

    try:
        retval = Popen(cmd, stdout=PIPE, stderr=STDOUT).communicate()[0]
        space_stripped = str(retval).strip()
        quote_stripped = str(space_stripped).strip("'")

    except Exception, err:
        logger.log(lp.VERBOSE, "Exception trying to get the console user...")
        logger.log(lp.VERBOSE, "Associated exception: " + str(err))
        logger.log(lp.WARNING, traceback.format_exc())
        logger.log(lp.WARNING, str(err))
        raise err
    else:
        """
        LANL's environment has chosen the regex below as a valid match for
        usernames on the network.
        """
        if re.match("^[A-Za-z][A-Za-z1-9_]+$", quote_stripped):
            user = str(quote_stripped)
    logger.log(lp.VERBOSE, "user: " + str(user))
    
    return user

###########################################################################

def touch(filename=""):
    """
    Python implementation of the touch command..
    
    """
    if re.match("^\s*$", filename) :
        logger.log(lp.INFO, "Cannot touch a file without a filename....")
    else :
        try:
            os.utime(filename, None)
        except:
            try :
                open(filename, 'a').close()
            except Exception, err :
                logger.log(lp.INFO, "Cannot open to touch: " + str(filename))

############################################################################

def getecho (fileDescriptor):
    """This returns the terminal echo mode. This returns True if echo is
    on or False if echo is off. Child applications that are expecting you
    to enter a password often set ECHO False. See waitnoecho().

    Borrowed from pexpect - acceptable to license
    """
    attr = termios.tcgetattr(fileDescriptor)
    if attr[3] & termios.ECHO:
        return True
    return False

############################################################################

def waitnoecho (fileDescriptor, timeout=3):
    """This waits until the terminal ECHO flag is set False. This returns
    True if the echo mode is off. This returns False if the ECHO flag was
    not set False before the timeout. This can be used to detect when the
    child is waiting for a password. Usually a child application will turn
    off echo mode when it is waiting for the user to enter a password. For
    example, instead of expecting the "password:" prompt you can wait for
    the child to set ECHO off::

        see below in runAsWithSudo

    If timeout is None or negative, then this method to block forever until
    ECHO flag is False.

    Borrowed from pexpect - acceptable to license
    """
    if timeout is not None and timeout > 0:
        end_time = time.time() + timeout
    while True:
        if not getecho(fileDescriptor):
            return True
        if timeout < 0 and timeout is not None:
            return False
        if timeout is not None:
            timeout = end_time - time.time()
        time.sleep(0.1)

###########################################################################

def isSaneFilePath(filepath):
    """
    Check for a good file path in the passed in string.
    
    @author: Roy Nielsen
    """
    sane = False
    if filepath and isinstance(filepath, basestring):
        if re.match("^[A-Za-z0-9_\-/\.]*", filepath):
            sane = True
    return sane

###########################################################################

