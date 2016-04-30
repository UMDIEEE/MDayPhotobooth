import os
import sys
import threading
import urllib.request

import time
from umdieeepb.engine.camera import PhotoBoothCameraEngine
from umdieeepb.engine.loading import PhotoBoothLoadingEngine

from PyQt5 import QtCore
#watercolor
class PhotoBoothEngine(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        
        self.loading_eng = PhotoBoothLoadingEngine()
        self.camera_eng = PhotoBoothCameraEngine()
        
        # States:
        #   0 = Loading/Setup (maybe increment this, logo = 1, this = 1... once all of this is done)
        #   1 = Camera / Live Filter Selection Screen
        #   2 = Preview Picture, ask for retake if necessary
        #   3 = Processing Photo Previews (for borders)
        #   4 = Preview and Select Picture Borders
        #   5 = Printing Options (how many?)
        #   6 = Printing Screen (delay X seconds)
        self.pbstate = 0
        
        self.stopnow = False
        
        self.running = True
        self.thread = threading.Thread(target=self.main)
        self.thread.start()
        
        self.signalmap = {
                            0:
                                {
                                    "url":    "qml/loading.qml",
                                    "engine": self.loading_eng,
                                    "master_signals":
                                        {
                                            self.on_status:     self.loading_eng.on_status
                                        },
                                    "method_signals":
                                        {
                                            self.loading_eng.on_status:     "status",
                                        },
                                    "internal_signals":
                                        {
                                            self.loading_eng.on_change_screen:       self.change_screen,
                                        },
                                },
                            1:
                                {
                                    "url":    "qml/main.qml",
                                    "engine": self.camera_eng,
                                    "master_signals":
                                        {
                                            self.on_status:                self.camera_eng.on_status,
                                            self.on_update_filter_preview: self.camera_eng.on_update_filter_preview
                                        },
                                    "method_signals":
                                        {
                                            self.camera_eng.on_status:                "status",
                                            self.camera_eng.on_update_filter_preview: "updateImageFilterPreview"
                                        },
                                    "internal_signals":
                                        {
                                            self.camera_eng.on_change_screen:        self.change_screen,
                                        },
                                }
                        }
    
    def _print(self, text):
        print("[PhotoBoothEngine] %s" % text)
    
    def main(self):
        self._print("Main started.")
        
        while not self.stopnow:
            self._print("Loop")
            
            #if self.pbstate == 0:
                #self.on_status.emit("Testing")
                #self.on_update_filter_preview.emit(1, "test-highlight.jpg")
                #self.on_change_url.emit('main.qml')
                
            time.sleep(3)
            
            #if self.pbstate == 0:
            #    self.change_screen(1)
            
    @QtCore.pyqtSlot(int)
    def change_screen(self, state):
        self.disconnect_state(self.pbstate)
        self.stop_state_thread(self.pbstate)
        self.pbstate = state
        self.change_qml(self.pbstate)
        self.connect_state(self.pbstate)
        self.start_state_thread(self.pbstate)
    
    def start_state_thread(self, state):
        self.signalmap[state]["engine"].start()
    
    def stop_state_thread(self, state):
        self.signalmap[state]["engine"].stop()
    
    def change_qml(self, state):
        qmlfile = self.signalmap[state]["url"]
        print("change_qml() called: " + qmlfile)
        self.on_change_url.emit(qmlfile)
    
    def connect_state(self, state):
        print("connect_state() called: state " + str(state))
        self.state_updateable = False
        print(self.signalmap[state]["internal_signals"])
        for signal in self.signalmap[state]["master_signals"]:
            signal.connect(self.signalmap[state]["master_signals"][signal])
        for signal in self.signalmap[state]["internal_signals"]:
            signal.connect(self.signalmap[state]["internal_signals"][signal])
        for signal in self.signalmap[state]["method_signals"]:
            self.on_connect_signal.emit(signal, self.signalmap[state]["method_signals"][signal])
    
    def disconnect_state(self, state):
        for signal in self.signalmap[state]["method_signals"]:
            signal.disconnect()
        for signal in self.signalmap[state]["internal_signals"]:
            signal.disconnect()
        for signal in self.signalmap[state]["master_signals"]:
            signal.disconnect()
    
    def stop(self):
        self.stopnow = True
    
    @QtCore.pyqtSlot()
    def start_download(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._download)
            thread.start()
    
    on_change_url = QtCore.pyqtSignal(str)
    on_connect_signal = QtCore.pyqtSignal(QtCore.pyqtBoundSignal, str)
    
    on_status = QtCore.pyqtSignal(str)
    on_update_filter_preview = QtCore.pyqtSignal(int, str)
    
