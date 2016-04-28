import sys
from PyQt5 import QtGui, QtQuick, QtWidgets, QtCore

from download import Downloader

downloader = Downloader('http://cdimage.debian.org/debian-cd/8.4.0/amd64/iso-cd/debian-8.4.0-amd64-netinst.iso')

app = QtWidgets.QApplication(sys.argv)
view = QtQuick.QQuickView()
view.rootContext().setContextProperty('downloader', downloader)
view.setSource(QtCore.QUrl("download.qml"))
view.show()
app.exec_()
