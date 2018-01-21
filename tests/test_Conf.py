#!/usr/bin/python

import re
import sys
import unittest

sys.path.append("../")

from lib.conf import Conf
from lib.loggers import CyLogger, LogPriority


class test_Conf(unittest.TestCase):
    """
    """
    @classmethod
    def setUpClass(self):
        """
        """
        self.logger = CyLogger()
        self.conf = Conf()
    
    @classmethod
    def tearDownClass(self):
        """
        """
        pass
    
    def test_version(self):
        """
        """
        self.conf.set_version("0.1.2")
        self.assertTrue(re.match("^0.1.2$", self.conf.get_version()))
        #####
        # Need to assert false cases -- Need input validation on setters..
        
    def test_prop_num(self):
        """
        """
        self.conf.set_prop_num("1234567")
        self.assertTrue(re.match("^\d\d\d\d\d\d\d$", self.conf.get_prop_num()))

    def test_user(self):
        """
        """
        self.conf.set_user("gandalf")
        self.assertTrue(re.match("^gandalf$", self.conf.get_user()))

    def test_password(self):
        """
        """
        self.assertRaises(TypeError, self.conf.set_password, 1)

        self.assertRaises(TypeError, self.conf.set_password, ["gandalf"])
        
        self.assertRaises(TypeError, self.conf.set_password, {"gandalf"})
        
        self.conf.set_password("gandalf")
        self.assertTrue(re.match("^gandalf$", self.conf.get_password()))

    def test_(self):
        """
        """
        self.assertTrue(True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
