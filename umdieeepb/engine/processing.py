import time
import threading
import os
from PyQt5 import QtCore

from umdieeepb.engine.stoppable import StoppableThread
from umdieeepb.mpworker import ImageProcessing, file_rename

class PhotoBoothProcessingLoadingEngine(QtCore.QObject, StoppableThread):
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
        print("[PhotoBoothProcessingLoadingEngine] %s" % text)
    
    def report_file_done(self, file_id, file_status):
        if file_status >= 2:
            pass
            #self.on_status.emit("%s %s" % (self.file_status[file_id], self.status_map[file_status]))
    
    def main(self, stop_queue):
        self._print("Main started.")
        
        time.sleep(3)
        
        self.on_status.emit("Building the wheatstone bridge...")
        
        self.file_status = {}
        self.mphelper = ImageProcessing(self.report_file_done)
        self.mphelper.start()
        
        self.counter = 1
        
        for f in os.listdir('assets/frames'):
            frame_path = os.path.join('assets/frames', f)
            if os.path.isfile(frame_path):
                new_path = "tmp/" + "frame_" + str(self.counter) + ".jpg"
                self.counter += 1
                print("%s -> %s" % (frame_path, new_path))
                self.file_status[self.mphelper.add_job(["frame_pic", "nice_image.jpg", frame_path, new_path])] = frame_path
        
        self.mphelper.finish_jobs()
        
        self.on_status.emit("Performing the Fourier transform at IEEE@UMD...")
        
        self.counter = 1
        
        for f in os.listdir('assets/frames'):
            frame_path = os.path.join('assets/frames', f)
            if os.path.isfile(frame_path):
                new_path = "tmp/" + "frame_" + str(self.counter) + ".jpg"
                new_path_mini = "tmp/" + "frame_mini_" + str(self.counter) + ".jpg"
                self.counter += 1
                print("%s -> %s" % (new_path, new_path_mini))
                self.file_status[self.mphelper.add_job(["shrink43Image", new_path, new_path_mini])] = new_path_mini
        
        self.mphelper.finish_jobs_and_reset()
        self.mphelper.stop()
        
        self.on_status.emit("Done!")
        time.sleep(1)
        self.on_change_screen.emit(4)
        #self.counter -= 1
        #self.on_change_url.emit('main.qml')
        #time.sleep(1)
    
    on_change_url = QtCore.pyqtSignal(str)
    on_status = QtCore.pyqtSignal(str)
    
    on_change_screen = QtCore.pyqtSignal(int)

