import QtQuick 2.5

Item {
    property string defaultText: "Hello, world!"
    property bool stateVisible: true
    property int targetX: 0
    property int targetY: 0
    
    id: textStatusItems
    
    width: parent.width
    height: parent.height
    
    focus: true
    
    Keys.onPressed: {
        console.log("Width: " + width);
        console.log("Height: " + height);
        console.log("X: " + x);
        console.log("Y: " + y);
        console.log("textBlock.x: " + textBlock.x);
        console.log("textBlock.y: " + textBlock.y);
        console.log("textBlock.opacity: " + textBlock.opacity);
        
        //stateVisible = !stateVisible
        //textBlock.y = (textBlock.y == parent.parent.height) ? (200) : parent.parent.height
        textBlock.moveUpLine()
        //textBlock.opacity = (textBlock.opacity == 0.0) ? 1.0 : 0.0
    }
    
    TextPopup {
        id: textBlock
        text: defaultText
        stateVisible: parent.stateVisible
        targetY: parent.height - textBlock.height
        autoFade: true
        destroyOnFade: true
        enableTransitions: true
    }
    
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onClicked: {
            console.log(width);
            console.log(height);
            
            parent.stateVisible = !parent.stateVisible
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
