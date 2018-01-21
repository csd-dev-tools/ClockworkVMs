#!/usr/bin/python -d

import sys
sys.path.append("..")

import unittest
from lib.tmp_enc import tmp_enc

class test_tmp_enc_xor_match(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """
        """
        self.tmpenc = tmp_enc()
        
    def test_one(self):
        """
        """
        self.assertFalse(self.tmpenc.xor_match("0", "0"))
        
    def test_two(self):
        """
        """
        self.assertTrue(self.tmpenc.crypt("abc321!@#"))
        
        self.assertTrue(self.tmpenc.xor_match("abc321!@#", str(self.tmpenc.password)))

    def test_three(self):
        """
        """
        self.assertFalse(self.tmpenc.xor_match("abc321!@#", "abc321!@#"))

if __name__ == "__main__":
    unittest.main()
