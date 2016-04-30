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
    
    Image {
        id: main
        x: 0
        y: 0
        width: 1440
        height: 900
        source: "../assets/background.png"
    }
    
    Rectangle {
        id: bgrect
        
        x: 0
        y: 0
        width: 1440
        height: 900
        
        color: "black"
        opacity: 0.6
    }
    Text {
        id: caption
        text: "Copies to Print:"
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
        anchors.centerIn: parent
    }
    
    Rectangle {
        id: rect
        
        color: "white"
        width: 200
        height: 100
        
        anchors.top: caption.bottom;
        anchors.margins: 20
        
        anchors.horizontalCenter: parent.horizontalCenter
        
        Text {
            id: number
            text: "1"
            font.family: "Helvetica"
            font.pointSize: 24
            color: "black"
            anchors.centerIn: parent
        }
    }
    
    Text {
        id: caption2
        text: "(Limit one copy per person!)"
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
        
        anchors.top: rect.bottom
        anchors.margins: 20
        anchors.horizontalCenter: parent.horizontalCenter
    }
    
    Text {
        id: caption3
        text: "Once you're ready, tap Finish!"
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
        
        anchors.top: caption2.bottom
        anchors.margins: 20
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
