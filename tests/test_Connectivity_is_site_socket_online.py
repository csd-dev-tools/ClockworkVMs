#!/usr/bin/python -d
import re
import sys
import unittest

### for importing support libraries
sys.path.append("../")

from lib.loggers import CyLogger
from lib.loggers import LogPriority as LP
from lib.Connectivity import Connectivity

##########################################################
#                        test#, expected, host
#                               result
test_case_data_one = \
{ "valid_connections": [("001", True, "www.lanl.gov"),
                        ("002", True, "www.google.com"),
                        ("003", True, "www.slashdot.org"),
                        ("004", True, "www.foxnews.com"),
                        ("005", True, "www.amazon.com"),
                       ],
  "invlaid_connections": [("010", False, "ha234567"),
                          ("011", False, "dab-tobor"),
                          ("012", False, "hgarblat"),
                         ],
}

##########################################################
#                        test#, expected, host, website
#                               result          path
test_case_data_two = \
{ "valid_connections": [("001", True, "http://www.lanl.gov:80", "/"),
                        ("002", True, "http://www.lanl.gov", "/"),
                        ],
  "invlaid_connections": [("010", False, "http://puppet.com", "/image"),
                          ("011", False, "http://www.lanl.gov", "/teamforge"),
                          ("012", False, "http://garblat", "/"),
                          ("013", False, "http://example", "/"),
                         ],
}

logger = CyLogger()

def name_test_template_one(*args):
    """ 
    decorator for monkeypatching
    """
    def foo(self):
        self.assert_value(*args)
    return foo 

class test_Connectivity_is_site_socket_online(unittest.TestCase):

    def setUp(self):
        self.conn = Connectivity(logger)
        self.conn.set_no_proxy()

    def assert_value(self, test_iteration, pass_or_not, host):

        if pass_or_not:
            self.assertTrue(self.conn.is_site_socket_online(host))
        else:
            self.assertFalse(self.conn.is_site_socket_online(host))


for behavior, test_cases in test_case_data_one.items():
    for test_case_data in test_cases:
        logger.log(LP.DEBUG, "test case data: " + str(test_case_data))
        test_iteration, pass_or_not, host = test_case_data
        my_test_name = "test_{0}_{1}".format(test_iteration, str(pass_or_not))
        my_test_case = name_test_template_one(*test_case_data)
        logger.log(LP.DEBUG, "test case data: " + str(my_test_case))
        setattr(test_Connectivity_is_site_socket_online, my_test_name, my_test_case)

if __name__ == "__main__":
    unittest.main()
