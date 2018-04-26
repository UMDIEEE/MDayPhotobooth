# Silly little Makefile to handle building the APK
# 
# For usage, type "make help"

# Update these variables if the version or naming changes
DBG_APK  = Photobooth-0.1-debug.apk
REL_APK  = Photobooth-0.1-release-unsigned.apk
REL_APKT = .buildozer/android/platform/python-for-android/dist/IEEE_UMD_Photobooth/bin/Photobooth-0.1-release-unsigned.apk
PKG_NAME = edu.umd.ece.ieee.photobooth.ieee_umd_photobooth

# Nothing should be changed beyond this point
ALL_DEPS = Makefile
APK_DEPS = buildozer.spec main.py

# Note that the all target MUST be the first target defined in order
# for it to be read... otherwise, it won't work!
all: debug release

.PHONY: all debug release clean distclean install uninstall uninstall-real redeploy redeploy-real

bin/$(DBG_APK): $(ALL_DEPS) $(APK_DEPS)
	buildozer --verbose android debug

bin/$(REL_APK): $(ALL_DEPS) $(APK_DEPS)
	buildozer --verbose android release || echo " - Build finished..."
	[ -f $(REL_APKT) ] && \
	  cp $(REL_APKT) bin/$(REL_APK)
	@echo " - Release build complete - the resulting APK can be found in"
	@echo "   bin/$(REL_APK)."
	@echo ""
	@echo "   Note that this APK must be signed and reorganized correctly"
	@echo "   (zipalign, see above messages) in order for installation and"
	@echo "   distribution to work."

debug: bin/$(DBG_APK)

release: bin/$(REL_APK)

clean:
	rm -f bin/*

distclean: clean
	rm -rf .buildozer

install: bin/$(DBG_APK)
	./wait_for_android_pm.sh
	# adb -r allows for reinstallation if it's already installed
	# This sometimes works, sometimes doesn't... but at the very least,
	# it increases the chance of success!
	adb install -r bin/$(DBG_APK)

uninstall:
	@echo "WARNING: Full uninstallation will require a device reboot."
	@echo "Run make uninstall-real to perform the uninstall."

uninstall-real:
	./wait_for_android_pm.sh
	adb shell pm list packages -f | grep $(PKG_NAME) && adb uninstall $(PKG_NAME) && adb reboot || echo "Package not installed, skipping uninstall step."

redeploy:
	@echo "WARNING: Redeploying will require a device reboot."
	@echo "Run make redeploy-real to perform the redeploy."

redeploy-real: uninstall-real install

help:
	@echo "Targets:"
	@echo
	@echo "  all (no argument): Build everything."
	@echo "  debug:             Build the debug APK."
	@echo "  release:           Build the release APK."
	@echo "  clean:             Remove built APKs."
	@echo "  distclean:         Remove built APKS and all build files."
	@echo "                     Note that if run, significant downloading"
	@echo "                     and build time will occur on next build."
	@echo "                     Use only as a last resort."
	@echo "  install:           Install/update the debug APK to the device."
	@echo "                     May fail if the package is already installed"
	@echo "                     on the Android device."
	@echo "  uninstall:         Uninstall the debug APK from the device."
	@echo "                     Requires a device reboot."
	@echo "  redeploy:          Redeploy the debug APK to the device."
	@echo "                     Requires a device reboot."
	@echo "  help:              Show this help."
	@echo
	@echo "Note that all Android device related commands require the device's"
	@echo "debugging support to be enabled, and for the correct Android"
	@echo "debugging tools to be installed."
	@echo
	@echo "The APK built by default is the debug APK, since this is the easiest"
	@echo "to build and install. The release APK requires signing."
