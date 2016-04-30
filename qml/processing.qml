import QtQuick 2.4

Rectangle {
    id: loadingProcessingWin
    
    width: 1440
    height: 900
    color: "black"
    
    Image {
        id: main
        x: 0
        y: 0
        width: 1440
        height: 900
        source: "../assets/background.png"
    }
    
    function status(statusText) {
        console.log("Got from python: status = "+statusText)
        textStatusBar.status(statusText)
    }
}
