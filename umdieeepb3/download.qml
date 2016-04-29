import QtQuick 2.4
import QtQuick.Controls 1.4

Rectangle {
    width: 200; height: 160

    Text {
        x: progressBar.x; y: 20
        width: progressBar.width
        font.pixelSize: 8
        text: downloader.filename
        elide: Text.ElideRight
    }

    ProgressBar {
        id: progressBar
        x: 20; y: 60
        width: parent.width-40

        value: downloader.progress
    }

    Button {
        anchors.left: progressBar.left
        anchors.right: progressBar.right

        y: progressBar.y + progressBar.height + 20

        text: downloader.running? "Please wait..." : "Start download"
        onClicked: { downloader.start_download() }
    }
}
