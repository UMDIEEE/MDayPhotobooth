# IEEE Maryland Day 2017 Photobooth Project

This branch contains a rewrite of the 2015 Photobooth project to
use Qt, a faster, more animated framework. The result was the 2016
Photobooth project.

For the latest 2017 Photobooth project, an actual control GUI was
created, and some important fixes were added!

## Changelog

 * **Photobooth 2017**:
 
   * New GUI:
     
     * A new GUI using Kivy was added that allows socket-based control
       from an Android tablet. This allows visitors to control the
       photobooth without an attendant. Previously, in 2016, the
       photobooth was controlled manually by an attendant by running
       commands to send the appropriate socket command to the
       photobooth.
     
     * The GUI implements all of the selection screens of the
       Photobooth, and each button sends the appropriate socket command.
       The GUI blocks the user from doing anything until the socket
       command completes.
   
   * Add email option to allow emailing the final photo to a
     user-specified email address. This includes the core functionality,
     as well as GUI changes and updates to make this work.
   
   * Temporarily disabled printing functionality, since we were unable
     to obtain a photo printer that year.
   
   * Fixed major issue with camera not showing up - this was due to the
     socket read blocking, causing state changes to not trigger a
     camera turn on. A fix was attempted in the past, but failed due to
     setting the nonblocking catch on the wrong part. The solution was
     to set up the nonblocking catch on the socket `accept()`. `read()`
     also has the nonblocking catch, but that is not as likely to
     trigger. Also added a state variable to only enable the camera once
     per state change.

 * **Photobooth 2016**:
 
   * Complete rewrite of GUI in PyQt and QML, allowing for a MUCH faster
     GUI on the Raspberry Pi screen.
   
   * Parallelization of the image processing done for the photobooth.
   
   * Keyboard control no longer exists, instead preferring a
     socket-based control interface. (This is also due to how QML works
     with keyboard input...)

## Project Changes
|               | Photobooth 2015                                                                                                                                                                 | Photobooth 2016-2017                                                                                                                                                         |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Core          | ImageMagick image processing; only able to process using single core, aka one image at a time                                                                                   | ImageMagick image processing; parallel image processing with multiple cores                                                                                                  |
| GUI           | Combination of ImageMagick, the `fbv` framebuffer image display tool, and Python curses input handling to create, draw, and manage input for the GUI (respectively). Very slow. | Entire GUI done in Qt5's QML and QtQuick. Qt5 uses GPU acceleration to make interface drawing easy and fast. Some interface effects added. Massive improvement over old GUI. |
| Functionality | Select a filter, take a photo, select a frame, print.                                                                                                                           | Select a filter, take a photo, confirm your photo, select a frame, select the number of copies, print, email (2017)                                                          |
| Code          | Messy, unorganized                                                                                                                                                              | Somewhat organized - GUI code is localized, split, and layered, other code is split up into proper parts                                                                     |

## Requirements
To run this photobooth, you need:

 * Raspberry Pi
 * Raspberry Pi OS (we used the latest Raspbian)
 * Python 3.x
 * Latest Qt 5.x
 * Latest PyQt compatible with the Qt 5.x
 * Python PiCamera library

## Running
Simply run `runpb.py` to get things going!

## Files

 * `assets/` - pictures needed by the program interface
 * `qml/` - QML interface files
   * Text Status Interface:
     * `TextPopup.qml` - basic text popup interface element. Used by
      `TextStatusFly.qml`.
     * `TextStatusFly.qml` - status update interface element, used for
      displaying progress and status messages.
     * `TextStatusFlyMaker.js` - Javascript library used in
       `TextStatusFly.qml` for dynamically creating `TextPopup`
       elements.
   * Screens:
     * `loading.qml` - initial loading screen. This is shown while
       frames are being resized.
     * `camera.qml` - photo taking screen. Filter selection takes place
       here.
     * `preview.qml` - photo previewing screen. You can confirm the
       photo taken here.
     * `processing.qml` - processing loading screen. This screen
       displays while the photo and available frames are being
       processed.
     * `frames.qml` - frame selection screen. Frames can be selected
       here.
     * `printopt.qml` - number of copies to be printed screen.
     * `emailopt.qml` - email to send to screen.
     * `printing.qml` - final "loading" screen, displaying messages
       indicating that printing is occuring.
     * `done.qml` - final "loading" screen, displaying messages
       indicating that emailing is occuring. Used in 2017 version in
       lieu of `printing.qml`.
 * `umdieeepb/` - main Python codebase.
   * `main.py` - main loop. Sets up the application, installs the
     right hooks to allow the application to work, and runs it.
   * Helper parts:
     * `mpworker.py` - super fast image processor for the photobooth.
       Parallelizes tough image processing tasks and gets batch jobs
       done pretty quickly.
       * This is one of the major changes with the new photobooth -
         much faster image processing!
     * `piprint.py` - printing module. Given a frame number and the
       number of times to print it, print the specified framed image.
     * `piemail.py` - email module. Given a frame number and the
       email to send the image to, email the specified framed image.
   * `engine/` - GUI engine parts. This segments different parts of
     the interface into many different parts, while still allowing
     some flow and connectivity. (This is another big feat with the
     new photobooth!)
     * `master.py` - master GUI engine that ties everything together.
       Main GUI "loop" for the entire photobooth that handles all of
       the screens displayed, as well as the communication between
       all of them. It ties the original main loop (`main.py`) to
       itself, and from itself to the screen engines. It also handles
       the internal state, and from that what should be shown at a
       given moment. It also handles the command processing, as well as
       the camera state.
     * Other files are direct links to their screens in QML, e.g.
       `umdieeepb/engine/emailopt.py` links directly to
       `qml/emailopt.qml` and handles signalling from there. For certain
       files, they handle the image processing necessary for the
       photobooth.
 * `runpb.py` - Photobooth launcher script. Loads `umdieeepb.main`
   modules, instantiates a `PhotoBoothGUI()` object, and calls its
   `run()` function.

## Internals

TODO

## Issues and TODO

## License

