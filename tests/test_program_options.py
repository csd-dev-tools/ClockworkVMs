#!/usr/bin/python -u
from __future__ import absolute_import
import unittest
import sys
import os
import re
import json
from collections import OrderedDict
from operator import itemgetter

appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
print "appendDir: " + appendDir
sys.path.append(appendDir)
from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp
from lib.run_commands import RunWith
from lib.program_options import ProgramOptions


parameter_dictionary = {'test1':[["-p", "proxy.example.com:8080"], {"rsyncProxy": "", "noProxy": "", "verbose": "False", "logPath": "/tmp/", "proxy": "proxy.example.com:8080", "debug": "False", "httpProxy": "", "repoRoot": "/opt/tools/src/boxcutter", "ftpProxy": "", "httpsProxy": ""}],
'test2':[[], {"rsyncProxy": "", "noProxy": "", "verbose": "False", "logPath": "/tmp/", "proxy": "", "debug": "False", "httpProxy": "", "repoRoot": "/opt/tools/src/boxcutter", "ftpProxy": "", "httpsProxy": ""}],
}


class test_program_options(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.logger = CyLogger(level=5)
        self.logger.initializeLogs()
        self.rw = RunWith(self.logger)
    @classmethod
    def tearDownClass(self):
        pass

    def test_params(self):
        
        for arg_set, expected in parameter_dictionary.iteritems():
            cmd = [os.path.dirname(os.path.abspath(__file__)) + '/program_options_mock.py'] + expected[0]
            self.logger.log(lp.DEBUG, "cmd: " + str(cmd))
            self.rw.setCommand(cmd)
            output, error, retval = self.rw.communicate()
            print output.strip()
            output_dict = json.loads(output.strip())
            self.assertTrue(expected[1] == output_dict, "Output doesn't match...")


if __name__ == "__main__":
    unittest.main()

