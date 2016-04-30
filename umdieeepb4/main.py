import sys
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

from PyQt5.QtQml import QQmlComponent, QQmlEngine

from engine.master import PhotoBoothEngine

class PhotoBoothGUI(QObject):
    def run(self):
        # Create main app
        self.myApp = QApplication(sys.argv)
        # Create a label and set its properties
        self.appLabel = QQuickView()
        #self.appLabel.setSource(QUrl('loading.qml'))

        # Show the Label
        self.appLabel.show()
        
        # Initialize PhotoBoothEngine.
        self.pbengine = PhotoBoothEngine()
        
        self.pbengine.on_change_url.connect(self.update_url_signal)
        self.pbengine.on_connect_signal.connect(self.connect_signal)
        
        self.pbengine.change_qml(0)
        self.pbengine.connect_state(0)
        
        
        print("UPDATE")
        #self.pbengine.on_status.connect(self.appLabel.rootObject().status)
        #self.pbengine.on_update_filter_preview.connect(self.appLabel.rootObject().updateImageFilterPreview)
        
        self.appLabel.rootContext().setContextProperty('pbengine', self.pbengine)

        self.setup_text_status_fly_component()
        
        self.pbengine.start_state_thread(0)
        
        # Execute the Application and Exit
        self.myApp.exec_()
        sys.exit()
    
    def setup_text_status_fly_component(self):
        # Create a component factory and load the QML script.
        print("Hello")
        self.component = QQmlComponent(self.appLabel.engine())
        self.component.loadUrl(QUrl('TextStatusFly.qml'))
        
        print("Hello2")
        self.statuswidget = self.component.create(self.appLabel.rootContext())
        
        print("Hello3")
        self.statuswidget.setParentItem(self.appLabel.rootObject())
        self.statuswidget.setParent(self.appLabel.rootObject())
        
        print("Hello4")
        #statuswidget.setProperty("targetX", 100)
        self.statuswidget.setProperty("objectName", "textStatusBar")
        
        print("Hello5")
        self.appLabel.rootContext().setContextProperty('textStatusBar', self.statuswidget)
        
        self.statuswidget.setProperty("parentSet", True)
    
    def update_url_signal(self, url):
        print(" ** Updating URL: %s" % url)
        
        #self.pbengine.on_change_url.disconnect()
        #self.pbengine.on_connect_signal.disconnect()
        
        self.appLabel.rootContext().setContextProperty('textStatusBar', None)
        self.appLabel.setSource(QUrl())
        self.appLabel.engine().clearComponentCache()
        self.appLabel.setSource(QUrl(url))
        self.setup_text_status_fly_component()
        self.appLabel.show()
        
        # Reconnect
        #self.pbengine.on_change_url.connect(self.update_url_signal)
        #self.pbengine.on_connect_signal.connect(self.connect_signal)
    
    def connect_signal(self, signal, target):
        print(" ** Binding signal %s to target %s!" % (str(signal), target))
        print(" ** (getattr(self.appLabel, target) = %s)" % (str(getattr(self.appLabel.rootObject(), target))))
        signal.connect(getattr(self.appLabel.rootObject(), target))

# Main Function
if __name__ == '__main__':
    pbgui = PhotoBoothGUI()
    pbgui.run()
