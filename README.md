# IEEE Maryland Day 2016 Photobooth Project

This branch contains a rewrite of last year's Photobooth project to
use Qt, a faster, more animated framework.

## Changes
|               | Photobooth 2015                                                                                                                                                                 | Photobooth 2016                                                                                                                                                              |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Core          | ImageMagick image processing; only able to process using single core, aka one image at a time                                                                                   | ImageMagick image processing; parallel image processing with multiple cores                                                                                                  |
| GUI           | Combination of ImageMagick, the `fbv` framebuffer image display tool, and Python curses input handling to create, draw, and manage input for the GUI (respectively). Very slow. | Entire GUI done in Qt5's QML and QtQuick. Qt5 uses GPU acceleration to make interface drawing easy and fast. Some interface effects added. Massive improvement over old GUI. |
| Functionality | Select a filter, take a photo, select a frame, print.                                                                                                                           | Select a filter, take a photo, confirm your photo, select a frame, select the number of copies, print                                                                        |
| Code          | Messy, unorganized                                                                                                                                                              | Somewhat organized - GUI code is localized, split, and layered, other code is split up into proper parts                                                                     |

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
     * `printing.qml` - final "loading" screen, displaying messages
       indicating that printing is occuring.
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
       given moment.
     * TODO
 * `runpb.py` - Photobooth launcher script. Loads `umdieeepb.main`
   modules, instantiates a `PhotoBoothGUI()` object, and calls its
   `run()` function.

## Internals

TODO
