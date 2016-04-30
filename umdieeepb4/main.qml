import QtQuick 2.4
//import QtQuick.Controls 1.3
import Qt.labs.controls 1.0
import QtQuick.Layouts 1.1

Rectangle {
    id: mainWin
    
    width: 1440
    height: 700/*900*/
    property alias filter6: filter6
    
    //property QtObject textStatusBar
    
    function status(statusText) {
        console.log("Got from python: status = "+statusText)
        textStatusBar.status(statusText)
    }
    
    function updateImageFilterPreview(filterNum, path) {
        console.log("Got from python: filterNum = " + filterNum + " | path = " + path)
        if (filterNum == 1) {
            console.log("NUMBA ONE REPORTING TO DUTY")
            filter1.source = path
        }
    }
    
    Component.onCompleted: {
        //mainWin.status.connect(textStatusBar.status)
        
    }
    
    function findChild(obj,objectName) {
        var childs = new Array(0);
        childs.push(obj)
        while (childs.length > 0) {
            if (childs[0].objectName == objectName) {
                return childs[0]
            }
            for (var i in childs[0].data) {
                childs.push(childs[0].data[i])
            }
            childs.splice(0, 1);
        }
        return null;
    }
    
    Keys.onPressed: {
        //console.log(findChild(mainWin, "textStatusBar"))
        console.log(textStatusBar.parent)
        
        console.log("MAIN: textStatusBar info:")
        console.log("MAIN: textStatusBar x = " + textStatusBar.x)
        console.log("MAIN: textStatusBar y = " + textStatusBar.y)
        console.log("MAIN: textStatusBar opacity = " + textStatusBar.opacity)
    }
    
    Image {
        id: main
        x: 420
        y: 0
        width: 600
        height: 900
        source: "test.jpg"
    }

    Image {
        id: filter1
        x: 0
        y: 0
        width: 210
        height: 315
        source: "test.jpg"
    }
    
    Image {
        id: filter2
        x: 210
        y: 0
        width: 210
        height: 315
        source: "test.jpg"
    }

    Image {
        id: filter3
        x: 0
        y: 315
        width: 210
        height: 315
        source: "test.jpg"
    }
    
    Image { 
        id: filter4
        x: 210
        y: 315
        width: 210
        height: 315
        source: "test.jpg"
    }

    Image { 
        id: logoleft
        x: 0
        y: 630
        width: 420
        height: 270
        //fillMode: Image.PreserveAspectFit
        source: "test.jpg"
    }

    Image {
        id: filter5
        x: 1020
        y: 0
        width: 211
        height: 315
        source: "test.jpg"
    }

    Image {
        id: filter6
        x: 1230
        y: 0
        width: 210
        height: 315
        source: "test.jpg"
    }

    Image {
        id: filter7
        x: 1020
        y: 315
        width: 210
        height: 315
        source: "test.jpg"
    }

    Image {
        id: filter8
        x: 1230
        y: 315
        width: 210
        height: 315
        source: "test.jpg"
    }

    Image {
        id: logoright
        x: 1020
        y: 630
        width: 420
        height: 270
        source: "test.jpg"
    }
}
