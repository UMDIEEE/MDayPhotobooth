import sys
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

from PyQt5.QtQml import QQmlComponent, QQmlEngine

from engine import PhotoBoothEngine

class PhotoBoothGUI(QObject):
    def run(self):
        # Create main app
        self.myApp = QApplication(sys.argv)
        # Create a label and set its properties
        self.appLabel = QQuickView()
        self.appLabel.setSource(QUrl('loading.qml'))
        #appLabel.load(QUrl('main2.qml'))

        # Show the Label
        self.appLabel.show()
        
        # Create a QML engine.
        self.engine = QQmlEngine()
        
        # Initialize PhotoBoothEngine.
        self.pbengine = PhotoBoothEngine()
        
        self.pbengine.on_change_url.connect(self.update_url_signal)
        
        print("UPDATE")
        self.pbengine.on_status.connect(self.appLabel.rootObject().status)
        #self.pbengine.on_update_filter_preview.connect(self.appLabel.rootObject().updateImageFilterPreview)
        
        self.appLabel.rootContext().setContextProperty('pbengine', self.pbengine)

        # Create a component factory and load the QML script.
        print("Hello")
        self.component = QQmlComponent(self.appLabel.engine())
        self.component.loadUrl(QUrl('TextStatusFly.qml'))
        
        print("Hello2")
        self.asdf = self.component.create(self.appLabel.rootContext())
        
        print("Hello3")
        self.asdf.setParentItem(self.appLabel.rootObject())
        self.asdf.setParent(self.appLabel.rootObject())
        
        print("Hello4")
        #asdf.setProperty("targetX", 100)
        self.asdf.setProperty("objectName", "textStatusBar")
        
        print("Hello5")
        self.appLabel.rootContext().setContextProperty('textStatusBar', self.asdf)
        
        self.asdf.setProperty("parentSet", True)
        
        #asdf.setProperty("y", 100)
        
        #print(appLabel)
        #print(appLabel.rootObject())
        #print(asdf)
        #print(asdf.x)
        #print(asdf.y)
        
        #block = appLabel.rootObject().create("TextPopup.qml", parent)
        #print(block)
        #block.x = 100
        #block.y = 200
        
        # Execute the Application and Exit
        self.myApp.exec_()
        sys.exit()
    
    def update_url_signal(self, url):
        print(" ** Updating URL: %s" % url)
        self.appLabel.setSource(QUrl(url))

# Main Function
if __name__ == '__main__':
    pbgui = PhotoBoothGUI()
    pbgui.run()
