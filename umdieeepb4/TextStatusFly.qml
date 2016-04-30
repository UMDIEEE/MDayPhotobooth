import QtQuick 2.5
import "TextStatusFlyMaker.js" as TextStatusFlyMaker

Item {
    property string defaultText: "Hello, world!"
    property bool stateVisible: true
    property int targetX: 0
    property int targetY: 0
    property bool parentSet: false
    
    function status(statusText) {
        console.log("LL Got from python: status = "+statusText)
        TextStatusFlyMaker.createTextPopupComponent(statusText);
    }
    
    id: textStatusItems
    
    //width: parent.width
    //height: parent.height
    
    focus: true
    
    Component.onCompleted: {
        //textStatusItems.status.connect(TextStatusFlyMaker.createTextPopupComponent)
        
    }
    
    Keys.onPressed: {
        console.log("Width: " + width);
        console.log("Height: " + height);
        console.log("X: " + x);
        console.log("Y: " + y);
        
        //stateVisible = !stateVisible
        //textBlock.y = (textBlock.y == parent.parent.height) ? (200) : parent.parent.height
        //textBlock.moveUpLine()
        //textBlock.opacity = (textBlock.opacity == 0.0) ? 1.0 : 0.0
    }
    
    /*TextPopup {
        id: textBlock
        text: defaultText
        stateVisible: parent.stateVisible
        targetY: parent.height - textBlock.height
        startY: parent.height //- textBlock.height
        autoFade: true
        destroyOnFade: true
        enableTransitions: true
        useTarget: true
    }*/
    
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onClicked: {
            console.log(width);
            console.log(height);
            
            parent.stateVisible = !parent.stateVisible
        }
    }
    
    /*Timer {
        id: sillyTimer
        interval: 3000
        running: true
        repeat: true
        onTriggered: {
            TextStatusFlyMaker.createTextPopupComponent("Hello, world!")
        }
    }*/
    
    Timer {
        id: parentSettingTimer
        interval: 100
        running: true
        repeat: true
        onTriggered: {
            if (parentSet) {
                width = parent.width
                height = parent.height
                parentSettingTimer.running = false
            }
            console.log("parentSet: " + parentSet)
        }
    }
    
    states: [
        State { when: stateVisible;
            PropertyChanges {   target: textStatusItems; opacity: 1.0; y: targetY    }
        },
        State { when: !stateVisible;
            PropertyChanges {   target: textStatusItems; opacity: 0.0; y: -height    }
        }
    ]
    transitions: Transition {
        reversible: true
        NumberAnimation { properties: "y,opacity"; duration: 500; easing.type: Easing.InOutQuad }
    }
    
    PropertyAnimation {
        id: animateY;
        target: textStatusItems;
        properties: "y";
        to: targetY;
        duration: 500
    }
}
