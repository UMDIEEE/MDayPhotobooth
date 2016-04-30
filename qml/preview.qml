import QtQuick 2.4
import QtGraphicalEffects 1.0

Rectangle {
    id: previewWin
    
    width: 1440
    height: 900
    
    property alias filter6: filter6
    
    //property QtObject textStatusBar
    
    function status(statusText) {
        console.log("Got from python: status = "+statusText)
        textStatusBar.status(statusText)
    }
    
    Image {
        id: main
        x: 0
        y: 0

        height: 900
        source: "nice_image.jpg"
    }
    
}
