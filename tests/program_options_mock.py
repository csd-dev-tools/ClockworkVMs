#!/usr/bin/python -u
from __future__ import absolute_import
from collections import OrderedDict
from operator import itemgetter
import json
import sys
import os
from collections import OrderedDict

appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-2])
#print "appendDir: " + appendDir
sys.path.append(appendDir)
import ClockworkVMs
from ClockworkVMs.lib.loggers import CyLogger
from ClockworkVMs.lib.loggers import LogPriority as lp
from ClockworkVMs.lib.run_commands import RunWith
from ClockworkVMs.lib.program_options import ProgramOptions

def acquireProgOptDict(programOptions=""):
    strippedString = programOptions.strip().strip("{").strip("}")
    progOptsData = strippedString.split(", ")
    progOpts = {}
    for item in progOptsData:
        (key, value) = item.split(": ")
        progOpts[key.strip("'")] = value.strip("'")

    return progOpts

progOpts = ProgramOptions()


programOptions = acquireProgOptDict(str(progOpts.options))

#print str(programOptions)

options = sorted(programOptions.items(),
                 key=itemgetter(1), 
                 reverse=True)

print str(options)
