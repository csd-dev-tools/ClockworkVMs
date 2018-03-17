from __future__ import absolute_import
import unittest
import time
import sys
import os
from datetime import datetime

appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(appendDir)

from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp
from lib.run_commands import RunWith, SetCommandTypeError


class test_run_commands(unittest.TestCase):
    """
    """

    @classmethod
    def setUpClass(self):
        """
        """
        #####
        # Set up logging
        self.logger = CyLogger(debug_mode=True)
        self.logger.initializeLogs()
        self.rw = RunWith(self.logger)
        #####
        # Start timer in miliseconds
        self.test_start_time = datetime.now()

    @classmethod
    def tearDownClass(self):
        """
        """
        pass

    def test_RunCommunicateWithBlankCommand(self):
        self.assertRaises(SetCommandTypeError, self.rw.setCommand, "")
        self.assertRaises(SetCommandTypeError, self.rw.setCommand, [])
        self.assertRaises(SetCommandTypeError, self.rw.setCommand, None)
        self.assertRaises(SetCommandTypeError, self.rw.setCommand, True)
        self.assertRaises(SetCommandTypeError, self.rw.setCommand, {})

    def test_setCommand(self):
        command = ['/bin/ls', 1, '.']
        self.assertRaises(SetCommandTypeError,
                          self.rw.setCommand, [command])

    def test_communicate(self):
        """
        """
        self.logger.log(lp.DEBUG, "=============== Starting test_communicate...")
        run_commands = ["/bin/ls /var/log/", ['/bin/ls', '-l', '/tmp/*']]
        i = 0

        self.logger.log(lp.DEBUG, "commands: " + str(run_commands))
        for command in run_commands:
            self.logger.log(lp.DEBUG, "command: " + str(command))
            self.rw.setCommand(command)
            _, _, retval = self.rw.communicate(silent=False)
            self.assertEquals(retval, 0,
                              "Valid [" + str(i) +
                              "] command execution failed: " +
                              str(command) + " --- retval: " + str(retval))
            i = i + 1

        self.rw.setCommand(['/bin/ls', '/1', '/'])
        _, _, retcode = self.rw.communicate()
        self.logger.log(lp.WARNING, "retcode: " + str(retcode))
        self.assertEquals(retcode, 1, "Returncode Test failed...")

        self.logger.log(lp.DEBUG, "=============== Ending test_communicate...")

    def test_wait(self):
        """
        """
        self.logger.log(lp.DEBUG, "=============== Starting test_wait...")
        run_commands = ["/bin/ls /var/log", ['/bin/ls', '-l', '/tmp/*']]
        i = 0

        self.logger.log(lp.DEBUG, "commands: " + str(run_commands))
        for run_command in run_commands:
            self.logger.log(lp.DEBUG, "command: " + str(run_command))
            self.rw.setCommand(run_command)
            _, _, retval = self.rw.wait(silent=False)
            self.assertEquals(retval, 0,
                              "Valid [" + str(i) +
                              "] command execution failed: " +
                              str(run_command))
            i = i + 1

        self.rw.setCommand(['/bin/ls', '/1', '/'])
        _, _, retcode = self.rw.wait()
        self.logger.log(lp.WARNING, "retcode: " + str(retcode))
        self.assertEquals(retcode, 1, "Returncode Test failed...")

    def test_waitNpassThruStdout(self):
        """
        """
        self.rw.setCommand(['/bin/ls', '/1', '/'])
        _, _, retcode = self.rw.waitNpassThruStdout()
        if sys.platform is 'darwin':
            self.assertEquals(retcode, 1, "Returncode Test failed...")
        else:
            self.assertEquals(retcode, 2, "Returncode Test failed...")

    def test_timeout(self):
        """
        """
        if os.path.exists("/sbin/ping"):
            ping = "/sbin/ping"
        elif os.path.exists('/bin/ping'):
            ping = "/bin/ping"

        self.rw.setCommand([ping, '8.8.8.8'])

        startTime = time.time()
        self.rw.timeout(3)
        elapsed = (time.time() - startTime)

        self.assertTrue(elapsed < 4,
                        "Elapsed time is greater than it should be...")

    def test_runAs(self):
        """
        """
        pass

    def test_liftDown(self):
        """
        """
        pass

    def test_runAsWithSudo(self):
        """
        """
        pass

    def test_runWithSudo(self):
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

    def test_RunThread(self):
        """
        """
        pass

    def test_runMyThreadCommand(self):
        """
        """
        pass


if __name__ == "__main__":

    unittest.main()


