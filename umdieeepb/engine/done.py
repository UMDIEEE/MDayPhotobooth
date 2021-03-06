import time
import threading
import os
from PyQt5 import QtCore

from umdieeepb.engine.stoppable import StoppableThread
from umdieeepb.mpworker import ImageProcessing, file_rename

class PhotoBoothDoneEngine(QtCore.QObject, StoppableThread):
    def __init__(self):
        QtCore.QObject.__init__(self)
        StoppableThread.__init__(self)
    
    def _print(self, text):
        print("[PhotoBoothDoneEngine] %s" % text)
    
    def main(self, stop_queue):
        self._print("Main started.")
        
        time.sleep(3)
        
        self.on_status.emit("Emailing all of the bits and pieces... (We're Emailing your photo(s) right now!)")
        
        time.sleep(1)
        
        self.on_status.emit("Please allow a few minutes to receive your photos.")
        
        time.sleep(1)
        
        self.on_status.emit("Thanks for visiting IEEE@UMD, and for coming this Maryland Day!")
        
        time.sleep(10)
        self.on_change_screen.emit(1)
    
    on_status = QtCore.pyqtSignal(str)
    
    on_change_screen = QtCore.pyqtSignal(int)

