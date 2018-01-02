from __future__ import absolute_import
import unittest
import sys
import os

if __name__ != "__main__":
    appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-2])
    print "appendDir: " + appendDir
    sys.path.append(appendDir)
    import ClockworkVMs
    from lib.loggers import CyLogger
    from lib.loggers import LogPriority as lp
    from lib.run_commands import RunWith

class Test_run_commands(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.logger = CyLogger()
        self.logger.initializeLogs()
        self.rw = RunWith(self.logger)
    @classmethod
    def tearDownClass(self):
        pass
    
    def test_RunCommunicateWithBlankCommand(self):
        self.assertRaises(ValueError, self.rw.setCommand, "")
        self.assertRaises(ValueError, self.rw.setCommand, [])
        self.assertRaises(TypeError, self.rw.setCommand, None)
        self.assertRaises(TypeError, self.rw.setCommand, True)
        self.assertRaises(TypeError, self.rw.setCommand, {})
        self.assertRaises(TypeError, self.rw.communicate, None)
        self.assertRaises(TypeError, self.rw.communicate, "")
        self.assertRaises(TypeError, self.rw.communicate, [])
        self.assertRaises(TypeError, self.rw.communicate, {})
        self.assertRaises(TypeError, self.rw.communicate, True)

    def test_ExecuteValidCommand(self):
        commands = ["/bin/ls /tmp/", ['/bin/ls', '-l', '/tmp/']]
        
        for command in commands:
            self.logger.log(lp.DEBUG, "command: " + str(command))
            self.rw.setCommand(command)
            output, error, retval = self.rw.communicate()
            self.assertTrue(retval, "Valid command execution failed: " + str(command))

    @unittest.SkipTest
    def test_ExecuteInvalidCommand(self):
        command = ['/bin/ls', 1, '.']
        self.rw.setCommand(command)
        self.assertRaises(TypeError, self.rw.communicate)
        self.assertRaises(TypeError, self.rw.waitNpassThruStdout)
        self.rw.setCommand('/bin/ls 1 .')
        self.assertRaises(OSError, self.rw.communicate, "Valid command execution failed.")
        self.assertFalse(OSError, self.rw.waitNpassThruStdout, "Valid command execution failed.")


if __name__ == "__main__":
    appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-2])
    print "appendDir: " + appendDir
    sys.path.append(appendDir)
    #import ClockworkVMs
    from ClockworkVMs.lib.loggers import CyLogger
    from ClockworkVMs.lib.loggers import LogPriority as lp
    from ClockworkVMs.lib.run_commands import RunWith

    unittest.main()

