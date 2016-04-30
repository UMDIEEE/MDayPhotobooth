import QtQuick 2.4

Rectangle {
    id: loadingProcessingWin
    
    width: 1440
    height: 900
    color: "black"
    
    function status(statusText) {
        console.log("Got from python: status = "+statusText)
        textStatusBar.status(statusText)
    }
}
