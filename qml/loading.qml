import QtQuick 2.4

Rectangle {
    id: loadingWin
    
    width: 1440
    height: 700/*900*/
    color: "black"
    
    function status(statusText) {
        console.log("Got from python: status = "+statusText)
        textStatusBar.status(statusText)
    }
    
    Keys.onPressed: {
        console.log(textStatusBar.parent)
        
        console.log("MAIN: textStatusBar info:")
        console.log("MAIN: textStatusBar x = " + textStatusBar.x)
        console.log("MAIN: textStatusBar y = " + textStatusBar.y)
        console.log("MAIN: textStatusBar opacity = " + textStatusBar.opacity)
    }
}
