import time
import threading
import os
from PyQt5 import QtCore

from umdieeepb.engine.stoppable import StoppableThread
from umdieeepb.mpworker import ImageProcessing

class PhotoBoothPreviewEngine(QtCore.QObject, StoppableThread):
    def __init__(self):
        QtCore.QObject.__init__(self)
        StoppableThread.__init__(self)
    
    def _print(self, text):
        print("[PhotoBoothPreviewEngine] %s" % text)
    
    def main(self, stop_queue):
        self._print("Main started.")
        
        #while not self.need_to_stop(stop_queue):
        time.sleep(3)
        self.on_status.emit("Done! If you like it, tap Continue. Otherwise, tap Back.")
    
    on_status = QtCore.pyqtSignal(str)
    
    on_change_screen = QtCore.pyqtSignal(int)

