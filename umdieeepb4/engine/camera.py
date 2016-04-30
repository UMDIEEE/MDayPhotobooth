from engine.stoppable import StoppableThread
import time

from PyQt5 import QtCore
#watercolor
class PhotoBoothCameraEngine(QtCore.QObject, StoppableThread):
    def __init__(self):
        QtCore.QObject.__init__(self)
        StoppableThread.__init__(self)
    
    def _print(self, text):
        print("[PhotoBoothCameraEngine] %s" % text)
    
    def main(self, stop_queue):
        self._print("Main started.")
        
        while not self.need_to_stop(stop_queue):
            self._print("Loop")
            self.on_status.emit("Testing")
            self.on_update_filter_preview.emit(1, "test-highlight.jpg")
            #self.on_change_url.emit('main.qml')
            time.sleep(1)
    
    on_change_url = QtCore.pyqtSignal(str)
    on_status = QtCore.pyqtSignal(str)
    on_update_filter_preview = QtCore.pyqtSignal(int, str)

