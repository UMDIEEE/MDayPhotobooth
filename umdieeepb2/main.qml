import QtQuick 2.4
//import QtQuick.Controls 1.3
import Qt.labs.controls 1.0
import QtQuick.Layouts 1.1

Rectangle {
    width: 1440
    height: 700/*900*/
    property alias filter6: filter6

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
        fillMode: Image.PreserveAspectFit
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
