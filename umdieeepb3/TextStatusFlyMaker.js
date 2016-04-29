var component;
var textPopupObjs = [];

function createTextPopupComponent(text) {
    if (component == null) {
        component = Qt.createComponent("TextPopup.qml");
    }
    if (component.status == Component.Ready)
        finishTextPopupComponent(text);
    else
        component.statusChanged.connect(finishCreation);
}

function finishTextPopupComponent(text) {
    if (component.status == Component.Ready) {
        var curTextPopupObj = component.createObject(textStatusItems, {
            "text": text,
            "stateVisible": parent.stateVisible,
            "targetY": parent.height - 60,
            "startY": parent.height, //- textBlock.height
            "autoFade": true,
            "destroyOnFade": true,
            "enableTransitions": true,
            "useTarget": true
        });
        if (curTextPopupObj == null) {
            // Error Handling
            console.log("Error creating object");
        }
        
        textPopupObjs.push(curTextPopupObj);
        console.log("curTextPopupObj.targetY: " + curTextPopupObj.targetY);
        console.log("curTextPopupObj.y: " + curTextPopupObj.y);
        moveUpAllTextPopups();
        
    } else if (component.status == Component.Error) {
        // Error Handling
        console.log("Error loading component:", component.errorString());
    }
}

function moveUpAllTextPopups() {
    for (var index = 0; index < textPopupObjs.length - 1; ++index) {
        if (textPopupObjs[index] != null)
            textPopupObjs[index].moveUpLine();
    }
}
