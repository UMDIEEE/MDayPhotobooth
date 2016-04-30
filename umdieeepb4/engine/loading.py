import time
import threading
from PyQt5 import QtCore

from engine.stoppable import StoppableThread

class PhotoBoothLoadingEngine(QtCore.QObject, StoppableThread):
    def __init__(self):
        QtCore.QObject.__init__(self)
        StoppableThread.__init__(self)
        
        self.counter = 3
    
    def _print(self, text):
        print("[PhotoBoothLoadingEngine] %s" % text)
    
    def main(self, stop_queue):
        self._print("Main started.")
        
        while not self.need_to_stop(stop_queue):
            self._print("Loop")
            self.on_status.emit("%i seconds left!" % self.counter)
            self.counter -= 1
            self.on_change_url.emit('main.qml')
            time.sleep(1)
    
    on_change_url = QtCore.pyqtSignal(str)
    on_status = QtCore.pyqtSignal(str)

