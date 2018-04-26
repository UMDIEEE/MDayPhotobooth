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
    
    function setEmail(email) {
        console.log("Got from python: email = " + email)
        email.text = email
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
        text: "Enter your Email:"
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
        anchors.centerIn: parent
    }
    
    Rectangle {
        id: rect
        
        color: "white"
        width: 400
        height: 100
        
        anchors.top: caption.bottom;
        anchors.margins: 20
        
        anchors.horizontalCenter: parent.horizontalCenter
        
        Text {
            id: number
            text: ""
            font.family: "Helvetica"
            font.pointSize: 24
            color: "black"
            anchors.centerIn: parent
        }
    }
    
    Text {
        id: caption2
        text: "We will email it to you ASAP!"
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
        
        anchors.top: rect.bottom
        anchors.margins: 20
        anchors.horizontalCenter: parent.horizontalCenter
    }
    
    Text {
        id: caption3
        text: "Once you're ready, tap Submit!"
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
        
        anchors.top: caption2.bottom
        anchors.margins: 20
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
