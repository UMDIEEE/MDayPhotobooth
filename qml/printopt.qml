import QtQuick 2.4
import QtGraphicalEffects 1.0

Rectangle {
    id: printOptWin
    
    width: 1440
    height: 900
    
    color: "black"
    
    function status(statusText) {
        console.log("Got from python: status = "+statusText)
        textStatusBar.status(statusText)
    }
    
    function setCopies(num) {
        console.log("Got from python: num = " + num)
        number.text = num
    }
    
    Text {
        id: caption
        text: "Copies to Print:\n(Limited to 1 per person!)"
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
        anchors.centerIn: parent
    }
    
    Text {
        id: number
        text: "1"
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
        anchors.centerIn: parent
    }
    
}