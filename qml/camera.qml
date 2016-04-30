import QtQuick 2.4
import QtGraphicalEffects 1.0

Rectangle {
    id: mainWin
    
    width: 1440
    height: 900
    property bool filter1_border: false
    property bool filter2_border: false
    property bool filter3_border: false
    property bool filter4_border: false
    property bool filter5_border: false
    property bool filter6_border: false
    property bool filter7_border: false
    property bool filter8_border: false
    
    property alias filter6: filter6
    
    //property QtObject textStatusBar
    
    function status(statusText) {
        console.log("Got from python: status = "+statusText)
        textStatusBar.status(statusText)
    }
    
    function updateImageFilterPreview(filterNum, path) {
        console.log("Got from python: filterNum = " + filterNum + " | path = " + path)
        if (filterNum == 1) {
            filter1.source = path
        }
    }
    
    function setBorderForImage(filterNum) {
        console.log("Got from python: filterNum = " + filterNum)
        if (filterNum == 1) filter1_border = true; else filter1_border = false
        if (filterNum == 2) filter2_border = true; else filter2_border = false
        if (filterNum == 3) filter3_border = true; else filter3_border = false
        if (filterNum == 4) filter4_border = true; else filter4_border = false
        if (filterNum == 5) filter5_border = true; else filter5_border = false
        if (filterNum == 6) filter6_border = true; else filter6_border = false
        if (filterNum == 7) filter7_border = true; else filter7_border = false
        if (filterNum == 8) filter8_border = true; else filter8_border = false
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
    
    ColorOverlay {
        anchors.fill: filter1_border ? filter1 : (filter2_border ? filter2 : (filter3_border ? filter3 : (filter4_border ? filter4 : (filter5_border ? filter5 : (filter6_border ? filter6 : (filter7_border ? filter7 : (filter8_border ? filter8 : filter8)))))))
        source: filter1_border ? filter1 : (filter2_border ? filter2 : (filter3_border ? filter3 : (filter4_border ? filter4 : (filter5_border ? filter5 : (filter6_border ? filter6 : (filter7_border ? filter7 : (filter8_border ? filter8 : filter8)))))))
        color: "#80800000"  // make image like it lays under red glass
    }
}
