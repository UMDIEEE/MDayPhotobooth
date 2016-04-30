from umdieeepb.engine.stoppable import StoppableThread
import time

from PyQt5 import QtCore
#watercolor
class PhotoBoothFramesEngine(QtCore.QObject, StoppableThread):
    def __init__(self):
        QtCore.QObject.__init__(self)
        StoppableThread.__init__(self)
        self.counter = 1
    
    def _print(self, text):
        print("[PhotoBoothFramesEngine] %s" % text)
    
    def main(self, stop_queue):
        self._print("Main started.")
        
        while not self.need_to_stop(stop_queue):
            self._print("Loop")
            time.sleep(1)
    
    on_change_screen = QtCore.pyqtSignal(int)
    
    on_status = QtCore.pyqtSignal(str)
    on_set_border_image = QtCore.pyqtSignal(int)

