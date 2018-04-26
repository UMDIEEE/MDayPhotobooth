# IEEE Maryland Day Photobooth Project - Android Control App

Created in the 2017 iteration of the Photobooth Project, this app
allows people to control the Photobooth from an Android tablet.

The Raspberry Pi Photobooth has a network socket control interface that
used to be controlled by an attendant via netcat'ing (`nc`) the correct
commands to the Raspberry Pi. With the Android control app, this is no
longer required, and photo takers get full control over their photo
taking experience!

## Usage

 1. Build and install the Android app to a tablet.
 2. Launch the app and ensure that the IP and port configuration is
    correct.
 3. Hand the tablet to the person who wants to take a photo. Guide them
    through each step until they reach the end!

## Requirements
The build should preferrably be done on Linux, though it may also work
on other platforms.

For building to work, you will need:

 * Python 3.x
 * Kivy
 * Buildozer, installed for Python 3.x (see [here][buildozer])
 * Android SDK/NDK/etc. (or space for installing these tools)
   * ADB should be installed and be in your PATH
 * Apache Ant
 * Java JDK
 * GCC (C, C++) Compiler

When installation of all components are complete, the total installation
size will be around 3-4 GBs.

## Build Instructions
To build everything, simply run:

    make

If you haven't installed the Buildozer dependencies before, the
Buildozer tool will automatically start the installation of said
dependencies. Dependencies are built and installed to both
`~/.buildozer` and `./.buildozer`.

Once you are done building, install the APK to your Android device by
running:

    make install

Note that your device MUST:

 * Have debugging enabled
 
 * Allow package installation from unknown sources
 
 * Allow debugging from the computer you plan on installing from

   * This is only required for newer Android versions. If you can run
     `adb shell` without any problems, then you should be good to go!

   * To allow debugging, unlock your device, run `adb shell`, and then
     tap "Allow" when the authorization popup shows up.

For other build/target options, run `make help`. A snapshot of the help
outputted can be found below:

    Targets:

      all (no argument): Build everything.
      debug:             Build the debug APK.
      release:           Build the release APK.
      clean:             Remove built APKs.
      distclean:         Remove built APKS and all build files.
                         Note that if run, significant downloading
                         and build time will occur on next build.
                         Use only as a last resort.
      install:           Install/update the debug APK to the device.
                         May fail if the package is already installed
                         on the Android device.
      uninstall:         Uninstall the debug APK from the device.
                         Requires a device reboot.
      redeploy:          Redeploy the debug APK to the device.
                         Requires a device reboot.
      help:              Show this help.

    Note that all Android device related commands require the device's
    debugging support to be enabled, and for the correct Android
    debugging tools to be installed.

    The APK built by default is the debug APK, since this is the easiest
    to build and install. The release APK requires signing.

## Issues and TODO
Issues with this app should be filed in our issue tracker!

A small TODO:

 * Add a hidden "master" mode - add a secret hidden button that allows
   booth volunteers to enter a "master" mode to change the scene pane
   to the right one, or change the IP/port settings. This button could
   be hidden in the top right corner, blending in completely with the
   background, and require 5 consecutive taps to trigger.

 * Format the last scene (email request) for better layout.
 
 * Reorganize all scenes to use BoxLayout.

 * Add printing scene.
 
 * Allow email scene to be skipped if printing is enabled.

## License
The license is the same license as the entire project (including the
photobooth code for the Raspberry Pi). For more details, see the
LICENSE file on the root of this repository.

[buildozer]: https://kivy.org/docs/guide/packaging-android.html
