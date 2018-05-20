#!/usr/bin/python
'''
Test for testing the libHelperFunctions library.
'''
import sys

sys.path.append("../")

import unittest
from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp


class test_libHelperFunctions(unittest.TestCase):
    """ 
    """

    @classmethod
    def setUpClass(self):
        """ 
        """
        self.logger = CyLogger(debug_mode=True)
        self.logger.initializeLogs()
        self.logger.log(lp.DEBUG, "Test " + self.__name__ + " initialized...")

    @classmethod
    def tearDownClass(self):
        """ 
        """
        pass

    def test_getConsoleUser(self):
        """ 
        """
        pass

    def test_touch(self):
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

    def test_isSaneFilePath(self):
        """ 
        """
        pass


