import os
import sys
import threading
import urllib.request

from PyQt5 import QtCore

class ScreenController(QtCore.QObject):
    def __init__(self, url, filename=None):
        QtCore.QObject.__init__(self)
        self._url = url
        if filename is None:
            filename = os.path.basename(self._url)
        self._filename = filename
        self._progress = 0.
        self._running = False
        self._size = -1
 
    def _download(self):
        print("Downloading!")
        def reporthook(pos, block, total):
            if self.size != total:
                self._size = total
                self.on_size.emit()
            self.progress = float(pos*block)/float(total)
            
            #print(self.progress)
            
            if self.progress == 100.0:
                print("Done!")
            
        urllib.request.urlretrieve(self._url, self._filename, reporthook)
        self.running = False
 
    @QtCore.pyqtSlot()
    def start_download(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._download)
            thread.start()
 
    def _get_progress(self):
        return self._progress
 
    def _set_progress(self, progress):
        self._progress = progress
        self.on_progress.emit()
 
    def _get_running(self):
        return self._running
 
    def _set_running(self, running):
        self._running = running
        self.on_running.emit()
 
    def _get_filename(self):
        return self._filename
 
    def _get_size(self):
        return self._size
 
    on_progress = QtCore.pyqtSignal()
    on_running = QtCore.pyqtSignal()
    on_filename = QtCore.pyqtSignal()
    on_size = QtCore.pyqtSignal()
 
    progress = QtCore.pyqtProperty(float, _get_progress, _set_progress,
                                notify=on_progress)
    running = QtCore.pyqtProperty(bool, _get_running, _set_running,
                                notify=on_running)
    filename = QtCore.pyqtProperty(str, _get_filename, notify=on_filename)
    size = QtCore.pyqtProperty(int, _get_size, notify=on_size)
