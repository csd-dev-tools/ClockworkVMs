import sys

from PyQt5 import QtWidgets

sys.path.append('..')

from lib.loggers import CyLogger
from ui.admin_creds import AdministratorCredentials

logger = CyLogger(debug_mode=True)
logger.initializeLogs()

app = QtWidgets.QApplication(sys.argv)

def setUserCreds(username='', password=''):
    print str(username)
    print str(password)

#####
# Get admin user credentials
adminCreds = AdministratorCredentials(logger)
adminCreds.userCreds.connect(setUserCreds)
adminCreds.ui.adminName.setText('Not Today Wabbit!')
adminCreds.ui.passwordLineEdit.setFocus()
adminCreds.show()
adminCreds.raise_()

app.exec_()


