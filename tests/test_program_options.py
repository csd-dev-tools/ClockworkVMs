#!/usr/bin/python -u
from __future__ import absolute_import
import unittest
import sys
import os
import re
from collections import OrderedDict
from operator import itemgetter

appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-2])
print "appendDir: " + appendDir
sys.path.append(appendDir)
import ClockworkVMs
from ClockworkVMs.lib.loggers import CyLogger
from ClockworkVMs.lib.loggers import LogPriority as lp
from ClockworkVMs.lib.run_commands import RunWith
from ClockworkVMs.lib.program_options import ProgramOptions


parameter_dictionary = {str(["-p", "proxyout.lanl.gov:8080"]):{'rsyncProxy': '', 'noProxy': '', 'verbose': False, 'logPath': '/tmp/', 'proxy': 'proxyout.lanl.gov:8080', 'debug': False, 'httpProxy': '', 'repoRoot': '/opt/tools/src/boxcutter', 'ftpProxy': '', 'httpsProxy': ''},
str([]):{'rsyncProxy': '', 'noProxy': '', 'verbose': False, 'logPath': '/tmp/', 'proxy': '', 'debug': False, 'httpProxy': '', 'repoRoot': '/opt/tools/src/boxcutter', 'ftpProxy': '', 'httpsProxy': ''},                
}


class test_program_options(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.logger = CyLogger(level=30)
        self.logger.initializeLogs()
        self.rw = RunWith(self.logger)
    @classmethod
    def tearDownClass(self):
        pass

    def test_params(self):
        
        for arg_set, expectedOut in parameter_dictionary.iteritems():
            arg_set1 = re.sub('"', '', arg_set)
            arg_set2 = re.sub("'", "", arg_set1)
            arg_set3 = arg_set2.strip("[")
            arg_set4 = arg_set3.strip("]")
            arg_set5 = arg_set4.split(", ")
            print str(arg_set5)
            cmd = [appendDir + "/ClockworkVMs/tests/program_options_mock.py"] + arg_set5
            self.logger.log(lp.DEBUG, "cmd: " + str(cmd))
            self.rw.setCommand(cmd)
            output, error, retval = self.rw.communicate()
            orderedOutput = output
            orderedExpectedoutput = OrderedDict([('verbose', 'False'), ('debug', 'False'), ('logPath', '/tmp/'), ('repoRoot', '/opt/tools/src/boxcutter'), ('rsyncProxy', ''), ('noProxy', ''), ('proxy', ''), ('httpProxy', ''), ('ftpProxy', ''), ('httpsProxy', '')])
            print "Output: " + str(orderedOutput)
            print "Expected: " + str(orderedExpectedoutput)
            #output, error, retval = self.rw.waitNpassThruStdout()
            
            self.assertEquals(set(orderedOutput), set(orderedExpectedoutput), "Problem executing command...")
            break

if __name__ == "__main__":
    unittest.main()

