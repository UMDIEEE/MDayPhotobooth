import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3

GridLayout {
    id: grid
    columns: 3

    Rectangle {
        width: 200
        height: 200

        MessageDialog {
            id: msg
            title: "Title"
            text: "Button pressed"
            onAccepted: visible = false
        }

        Button {
            x:66; y:93

            /* adjust rectangle dimension based on text size */
            text: "Hello World"
            onClicked: {
                msg.visible = true
                /*console.log("Text width: " + buttonTxt.width)
                console.log("Text height: " + buttonTxt.height)*/
            }
            style: ButtonStyle {
                background: Rectangle {
                    // our border
                    border.width: 2;
                    border.color: "gray"
                    radius: 4; smooth: true
                    gradient: Gradient { // background gradient
                        GradientStop { position: control.pressed ? 1.0 : 0.0; color: "#353535" }
                        GradientStop { position: control.pressed ? 0.0 : 1.0; color: "black" }
                    }
                }
                label: Component {
                    Text {
                        id: btntext // object id of this text
                        color: "white"
                        text: control.text
                        // center the text on parent
                        anchors.horizontalCenter:parent.horizontalCenter;
                        anchors.verticalCenter:parent.verticalCenter;
                        font.pointSize: 20
                    }
                }
            }
            /*width: (btntext.width+16);
            height: (btntext.height+16)*/
        }
    }
}

