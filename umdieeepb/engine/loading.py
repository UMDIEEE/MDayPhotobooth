import time
import threading
import os
from PyQt5 import QtCore

from umdieeepb.engine.stoppable import StoppableThread
from umdieeepb.mpworker import ImageProcessing

class PhotoBoothLoadingEngine(QtCore.QObject, StoppableThread):
    def __init__(self):
        QtCore.QObject.__init__(self)
        StoppableThread.__init__(self)
        
        self.counter = 3
        
        self.status_map = {
                0: "Not started yet",
                1: "Compressing image",
                2: "Failed to compress image",
                3: "Suceesfully compressed image"
            }
    
    def _print(self, text):
        print("[PhotoBoothLoadingEngine] %s" % text)
    
    def report_file_done(self, file_id, file_status):
        if file_status >= 2:
            pass
            #self.on_status.emit("%s %s" % (self.file_status[file_id], self.status_map[file_status]))
    
    def main(self, stop_queue):
        self._print("Main started.")
        
        self.on_status.emit("Creating circuit diagrams...")
        
        self.file_status = {}
        self.mphelper = ImageProcessing(self.report_file_done)
        self.mphelper.start()
        
        for f in os.listdir('assets/frames'):
            orig_path = os.path.join('assets/frames', f)
            if os.path.isfile(orig_path):
                new_path = "assets/frames/preview/" + f
                print("%s -> %s" % (orig_path, new_path))
                self.file_status[self.mphelper.add_job(["shrink43Image", orig_path, new_path])] = orig_path
        self.mphelper.finish_jobs_and_reset()
        
        self.on_status.emit("Done!")
        time.sleep(1)
        self.on_change_screen.emit(1)
        #self.counter -= 1
        #self.on_change_url.emit('main.qml')
        #time.sleep(1)
    
    on_change_url = QtCore.pyqtSignal(str)
    on_status = QtCore.pyqtSignal(str)
    
    on_change_screen = QtCore.pyqtSignal(int)

