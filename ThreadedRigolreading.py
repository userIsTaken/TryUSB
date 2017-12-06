from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys, os
from USBTMC_Devices import *
from GetInfoAboutDevices import *
from ConfigParser import *
import vxi11

class RigolBackGround_scanner(QRunnable):
        def __init__(self):
                super().__init__()
                pass

