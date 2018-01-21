#!/usr/bin/python -d
import sys
import unittest

### for importing support libraries
sys.path.append("../")

from lib.loggers import CyLogger
from lib.loggers import LogPriority as LP
from lib.Connectivity import Connectivity

##########################################################
#                        test#, expected, host, website
#                               result          path
test_case_data_two = \
{ "valid_connections" : [(True, "001", """http://www.google.com/"""),
                         (True, "002", """http://int.lanl.gov"""),
                        ],
  "invlaid_connections" : [(False, "010", """http://-----/--"""),
                           (False, "011", """http://-----:8000/"""),
                           (False, "012", """http://example/"""),
                          ],
}

logger = CyLogger()

def name_test_template(*args):
    """ 
    decorator for monkeypatching
    """
    def foo(self):
        self.assert_value(*args)
    return foo 

class test_Connectivity_is_page_available(unittest.TestCase):

    def setUp(self):
        self.conn = Connectivity(logger)
        self.conn.set_no_proxy()

    def assert_value(self, expected, test_iteration, site):

        if expected:
            self.assertTrue(self.conn.isPageAvailable(site))
        else:
            self.assertFalse(self.conn.isPageAvailable(site))


#for test_cases in test_case_data_two.items():
for behavior, test_cases in test_case_data_two.items():
    for test_case_data in test_cases:
        logger.log(LP.DEBUG, "test case data: " + str(test_case_data))
        expected, test_iteration, site = test_case_data
        my_test_name = "test_{2}_{0}_{1}".format(test_iteration, str(expected), str(behavior))
        my_test_case = name_test_template(*test_case_data)
        setattr(test_Connectivity_is_page_available, my_test_name, my_test_case)

if __name__ == "__main__":
    unittest.main()
