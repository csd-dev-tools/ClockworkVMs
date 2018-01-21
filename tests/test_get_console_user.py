"""
Can test in python 2.7 and later...
"""
import re
import sys
import unittest
#from mock import *

### import .. to be able to import the following:
sys.path.append("..")
from lib.libHelperFunctions import get_console_user

test_case_data = \
{ "valid_possible_username" :   [("001", True, "ALLCAPS"),
                                 ("002", True, "z1234567"),
                                 ("003", True, "ab_CDE"),
                                 ("004", True, "Blart67"),
                                 ("005", True, "dcsadmin"),
                                ],  
  "console_user_value" :        [("000functional_test", True, str(get_console_user())),],
  "invalid_possible_username" : [("010", False, "%glarf"),
                                 ("011", False, "foo*bar"),
                                 ("012", False, "foo*bar^"),
                                 ("013", False, "^foo*bar"),
                                 ("014", False, "@foo*bar"),
                                 ("015", False, "fo@*bar"),
                                 ("016", False, "!foo*bar"),
                                 ("017", False, "foo*bar!"),
                                 ("018", False, "-1234567"),
                                 ("019", False, "'1234567'"),
                                 ("020", False, "_1234567"),
                                ],  
 } 

def name_test_template(*args):
    """ 
    decorator for monkeypatching
    """
    def foo(self):
        self.assert_value(*args)
    return foo 

class test_get_console_user(unittest.TestCase):

    def assert_value(self, test_iteration, pass_or_not, name):
        """
        Regex string below is valid usernames on Mac at LANL.  
        """
        if pass_or_not:
            self.assertRegexpMatches(name, "^[A-Za-z][1-9A-Za-z_]+$")
        else:
            self.assertNotRegexpMatches(name, "^[A-Za-z][1-9A-Za-z_]+$")


for behavior, test_cases in test_case_data.items():
    for test_case_data in test_cases:
        test_iteration, pass_or_not, name = test_case_data
        my_test_name = "test_{0}_{1}_{2}".format(test_iteration, str(pass_or_not), str(name))
        my_test_case = name_test_template(*test_case_data)
        setattr(test_get_console_user, my_test_name, my_test_case)

