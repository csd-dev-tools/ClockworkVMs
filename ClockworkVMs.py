#!/usr/bin/python

import os
import re
import sys
import time

#####
# app specific files
from lib.conf import Conf
from lib.run_commands import RunWith
from lib.loggers import LogPriority as lp
from lib.program_options import ProgramOptions
from lib.CheckApplicable import CheckApplicable

#####
# import PyQt libraries
# from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

#####
# Import main gui
#from ui.Work import Work
from ui.VirtualMachineBuilder import VirtualMachineBuilder

def main():
    """
    Main program

    @author: Roy Nielsen
    """
    prog_opts = ProgramOptions()
    conf = prog_opts.returnConf()
    conf.loggerSelf()
    environ = conf.getEnviron()

    logger = conf.getLogger()
    #print str(logger)
    rw = RunWith(logger)
    logger.log(lp.INFO, "#==--- Initializing VmBuilder.app ---==#")

    #####
    # Instantiate & execute application...
    app = QtWidgets.QApplication(sys.argv)

    '''
    #####
    # Set up dialog
    mydialog = Work(conf)
    mydialog.setOpenExternalLinks(True)
    mydialog.setWindowTitle("Vm Builder")
    mydialog.show()
    mydialog.raise_()
    '''

    mydialog = VirtualMachineBuilder(conf)
    mydialog.setOpenExternalLinks(True)
    #mydialog.setModal(True)
    mydialog.setWindowTitle("Virtual Machine Builder")
    if mydialog.exec_():
        #mydialog.show()
        mydialog.raise_()
    '''
    if mydialogRetval == mydialog.Accepted:
        logger.log(lp.DEBUG, "Dialog accepted...")
        mydialogRetval = mydialog.exec_()
        mydialog.raise_()
    elif mydialogRetval == mydialog.Rejected:
        logger.log(lp.DEBUG, "Dialog rejected...")
        app.closeAllWindows()
    '''
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())

