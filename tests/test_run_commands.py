import sys

sys.path.append("../")

import unittest
from datetime import datetime
from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp


class test_run_commands(unittest.TestCase):
    """
    """

    @classmethod
    def setUpClass(self):
        """
        """
        #####
        # Set up logging
        self.logger = CyLogger()
        #####
        # Start timer in miliseconds
        self.test_start_time = datetime.now()



    @classmethod
    def tearDownClass(self):
        """
        """
        pass

    def test_system_call(self):
        """
        """
        pass

    def test_system_call_retval(self):
        """
        """
        pass

    def test_exec_subproc_stdout(self):
        """
        """
        pass

    def test_runWithWaitTillFinished(self):
        """
        """
        pass

    def test_kill_proc(self):
        """
        """
        pass

    def test_runWithTimeout(self):
        """
        """
        pass

    def test_runWithPty(self):
        """
        """
        pass

    def test_runAs(self):
        """
        """
        pass

    def test_getecho(self):
        """
        """
        pass

    def test_waitnoecho(self):
        """
        """
        pass

    def test_runAsWithSudo(self):
        """
        """
        pass

    def test_RunThread(self):
        """
        """
        pass

    def test_runMyThreadCommand(self):
        """
        """
        pass

