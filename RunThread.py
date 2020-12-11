# -*- coding: utf-8 -*-
import os
from PyQt5 import QtCore

class runThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)
    
    def __init__(self, execStr):
        super(runThread, self).__init__()
        self.execStr = execStr
        
        
    def run(self):
        
        outputText = os.popen(self.execStr).read()
        outStr = "This program begin !\n"
        outStr += outputText
        outStr += "\nAll have been finished !"
        self.trigger.emit(outStr)
        
        
        
