#!/usr/bin/python -u
from __future__ import absolute_import
from collections import OrderedDict
from operator import itemgetter
import json
import sys
import os
from collections import OrderedDict

mydir = os.path.dirname(os.path.abspath(__file__))
parentdir = "/" + "/".join(mydir.split("/")[:-1])
print parentdir
sys.path.append(parentdir)

from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp
from lib.run_commands import RunWith
from lib.program_options import ProgramOptions

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
