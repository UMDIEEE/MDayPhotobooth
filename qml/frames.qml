import QtQuick 2.4
import QtGraphicalEffects 1.0

Rectangle {
    id: frameWin
    
    width: 1440
    height: 900
    property bool frame1_border: true
    property bool frame2_border: false
    property bool frame3_border: false
    property bool frame4_border: false
    property bool frame5_border: false
    property bool frame6_border: false
    property bool frame7_border: false
    property bool frame8_border: false
    
    property alias frame6: frame6
    
    //property QtObject textStatusBar
    
    function status(statusText) {
        console.log("Got from python: status = "+statusText)
        textStatusBar.status(statusText)
    }
    
    function updateImageFilterPreview(frameNum, path) {
        console.log("Got from python: frameNum = " + frameNum + " | path = " + path)
        if (frameNum == 1) {
            frame1.source = path
        }
    }
    
    function setBorderForImage(frameNum) {
        console.log("Got from python: frameNum = " + frameNum)
        if (frameNum == 1) frame1_border = true; else frame1_border = false
        if (frameNum == 2) frame2_border = true; else frame2_border = false
        if (frameNum == 3) frame3_border = true; else frame3_border = false
        if (frameNum == 4) frame4_border = true; else frame4_border = false
        if (frameNum == 5) frame5_border = true; else frame5_border = false
        if (frameNum == 6) frame6_border = true; else frame6_border = false
        if (frameNum == 7) frame7_border = true; else frame7_border = false
        if (frameNum == 8) frame8_border = true; else frame8_border = false
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
        console.log(textStatusBar.parent)
        
        console.log("MAIN: textStatusBar info:")
        console.log("MAIN: textStatusBar x = " + textStatusBar.x)
        console.log("MAIN: textStatusBar y = " + textStatusBar.y)
        console.log("MAIN: textStatusBar opacity = " + textStatusBar.opacity)
    }
    
    Image {
        id: invisible
        width: 0
        height: 0
    }
    
    Image {
        id: main
        x: 420
        y: 0
        width: 600
        height: 900
        source: frame1_border ? "../tmp/frame_1.jpg" : (frame2_border ? "../tmp/frame_2.jpg" : (frame3_border ? "../tmp/frame_3.jpg" : (frame4_border ? "../tmp/frame_4.jpg" : (frame5_border ? "../tmp/frame_5.jpg" : (frame6_border ? "../tmp/frame_6.jpg" : (frame7_border ? "../tmp/frame_7.jpg" : (frame8_border ? "../nice_image.jpg" : "")))))))
    }

    Image {
        id: frame1
        x: 0
        y: 0
        width: 210
        height: 315
        source: "../tmp/frame_mini_1.jpg"
    }
    
    Image {
        id: frame2
        x: 210
        y: 0
        width: 210
        height: 315
        source: "../tmp/frame_mini_2.jpg"
    }

    Image {
        id: frame3
        x: 0
        y: 315
        width: 210
        height: 315
        source: "../tmp/frame_mini_3.jpg"
    }
    
    Image { 
        id: frame4
        x: 210
        y: 315
        width: 210
        height: 315
        source: "../tmp/frame_mini_4.jpg"
    }

    Image { 
        id: logoleft
        x: 0
        y: 630
        width: 420
        height: 270
        //fillMode: Image.PreserveAspectFit
        source: "../assets/left_logo.png"
    }

    Image {
        id: frame5
        x: 1020
        y: 0
        width: 211
        height: 315
        source: "../tmp/frame_mini_5.jpg"
    }

    Image {
        id: frame6
        x: 1230
        y: 0
        width: 210
        height: 315
        source: "../tmp/frame_mini_6.jpg"
    }

    Image {
        id: frame7
        x: 1020
        y: 315
        width: 210
        height: 315
        source: "../tmp/frame_mini_7.jpg"
    }

    Image {
        id: frame8
        x: 1230
        y: 315
        width: 210
        height: 315
        source: "../nice_image.jpg"
    }

    Image {
        id: logoright
        x: 1020
        y: 630
        width: 420
        height: 270
        source: "../assets/right_logo.jpg"
    }
    
    ColorOverlay {
        anchors.fill: frame1_border ? frame1 : (frame2_border ? frame2 : (frame3_border ? frame3 : (frame4_border ? frame4 : (frame5_border ? frame5 : (frame6_border ? frame6 : (frame7_border ? frame7 : (frame8_border ? frame8 : invisible)))))))
        source: frame1_border ? frame1 : (frame2_border ? frame2 : (frame3_border ? frame3 : (frame4_border ? frame4 : (frame5_border ? frame5 : (frame6_border ? frame6 : (frame7_border ? frame7 : (frame8_border ? frame8 : invisible)))))))
        color: "#80800000"  // make image like it lays under red glass
    }
}
