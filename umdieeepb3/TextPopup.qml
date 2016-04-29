import QtQuick 2.5

Rectangle {
    property string text: "Hello, world!"
    property bool stateVisible: true
    property bool autoFade: false
    property bool destroyOnFade: false
    property bool enableTransitions: false
    property bool useTarget: false // This needs to be set to enable everything
    property bool actuallyStart: false
    property int targetX: 0
    property int targetY: 0
    property int startX: 0
    property int startY: 0
    
    signal moveUpLine()
    signal startFadeTimer()
    
    Component.onCompleted: {
        /*textPopupRect.animAll.connect(doAnimAll)
        textPopupRect.animY.connect(doAnimY)
        textPopupRect.animOpacity.connect(doAnimOpacity)*/
        
        textPopupRect.moveUpLine.connect(doMoveUpLine)
        
        console.log("Startup")
        propTimer.running = true
        console.log("Startup end")
    }
    
    function doMoveUpLine() {
        targetY = targetY - height
        y = targetY
    }
    
    id: textPopupRect
    color: "black"
    opacity: 0.0
    
    /*anchors.centerIn: parent*/
    width: childrenRect.width + 20
    height: childrenRect.height + 20
    
    x: targetX
    y: (targetY == 0) ? -height : targetY
    
    focus: true
    
    Keys.onPressed: {
        console.log("Popup Width: " + width);
        console.log("Popup Height: " + height);
        console.log("Popup X: " + x);
        console.log("Popup Y: " + y);
        
        //stateVisible = !stateVisible
    }
    
    Timer {
        id: propTimer
        interval: 100; running: false; repeat: true
        onTriggered: {
            console.log("propTimer trigger")
            if (useTarget) {
                y = (startY == 0) ? (-height) : startY
                
                console.log("targetY set to: " + targetY)
                console.log("y set to: " + y)
                
                yBehavior.enabled = enableTransitions
                opacityBehavior.enabled = enableTransitions
                
                console.log("Enabled: " + yBehavior.enabled + " and " + opacityBehavior.enabled)
                
                actuallyStart = true
                
                fadeTimer.running = autoFade
                propTransTimer.running = true
                propTimer.running = false
            }
        }
    }
    
    Timer {
        id: propTransTimer
        interval: 10; running: false; repeat: true
        onTriggered: {
            console.log("propTransTimer: executing")
            console.log("propTransTimer old y = "+y)
            console.log("propTransTimer | targetY = "+targetY)
            y = (targetY == 0) ? (-height) : targetY
            console.log("propTransTimer assigns y = "+y)
        }
    }
    
    Timer {
        id: fadeTimer
        interval: 5000; running: false; repeat: false
        onTriggered: {
            opacity = 0.0
            destroyTimer.running = destroyOnFade
        }
    }
    
    Timer {
        id: destroyTimer
        interval: 1000; running: false; repeat: false
        onTriggered: {
            //console.log("Destroying...")
            //textPopupRect.destroy()
        }
    }
    
    Text {
        id: textPopupTxt
        
        /*anchors.fill: parent*/
        anchors.centerIn: parent
        
        width: paintedWidth
        height: paintedHeight
        
        text: parent.text
        font.family: "Helvetica"
        font.pointSize: 24
        color: "white"
    }
    
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onClicked: {
            /*
            if (mouse.button == Qt.RightButton)
                parent.color = 'blue';
            else
                parent.color = 'red';
            */
            console.log(width);
            console.log(height);
            
            //parent.stateVisible = !parent.stateVisible
        }
    }
    
    states: [
        State { when: stateVisible;
            PropertyChanges {   target: textPopupRect; opacity: actuallyStart ? 1.0 : 0.0;    }
        },
        State { when: !stateVisible;
            PropertyChanges {   target: textPopupRect; opacity: 0.0;    }
        }
    ]
    /*transitions: Transition {
        reversible: true
        NumberAnimation { property: "opacity"; duration: 500; easing.type: Easing.InOutQuad }
    }*/
    
    Behavior on y {
        id: yBehavior
        enabled: false
        PropertyAnimation {
            id: animateY
            duration: 500
            easing.type: Easing.InOutQuad
        }
    }
    
    Behavior on opacity {
        id: opacityBehavior
        enabled: false
        NumberAnimation {
            id: animateOpacity
            duration: 500
            easing.type: Easing.InOutQuad
        }
    }
}
