# This is code for raspberry pi to take a picture with a button

from time import sleep #library to control speed of project
import picamera #library to use camera with Python
import RPi.GPIO as GPIO #library to use the GPIO pins with Python (looking at Pins 6 and 8 for Ground and GPIO14)
import subprocess
import dummymp
from framesupport import *

dummymp.set_max_processes(4)

def drawFOverlayImage(images, highlightIndex, output_file):
	initialArgs = ['convert', '-size', '1920x1080', 'xc:black']
	curIndex = 0
	
	addlArgs = []
	xOffset = 0
	yOffset = 0
	for image in images:
		if curIndex > 3:
			xOffset = -1920
			yOffset = 540
		if curIndex == highlightIndex:
			sizing_output = subprocess.check_output(['identify', image])
			sizing_arr = [ int(j) for j in sizing_output.split(" ")[2].split('x') ]
			rectangleArg = "rectangle %i,%i,%i,%i" % ((480 * curIndex) + xOffset, yOffset, xOffset + (480 * curIndex) + sizing_arr[0]+8, sizing_arr[1]+8 + yOffset)
			addlArgs += [ '-fill', 'red', '-draw', rectangleArg ]
		geoArg = "+%i+%i" % (xOffset + 4 + (480 * curIndex), (4 + yOffset))
		addlArgs += [ image, '-geometry', geoArg, "-composite" ]
		curIndex += 1
	addlArgs += [ output_file ]	
	s = subprocess.Popen(initialArgs + addlArgs)
	s.communicate()

def showFOverlayImage(highlightIndex):
	s = subprocess.Popen(["/home/pi/MDay2015/bgimage", "temp/output-frame-"+str(highlightIndex)+".png"])
	s.communicate()

def pickFrameImages(images):
	try:
		initCurses()
		i = 0
		screen.refresh()
		showFOverlayImage(i)
		
		for i in xrange(0, len(images)):
			dummymp.run(drawFOverlayImage, images, i, "temp/output-frame-"+str(i)+".png")
	
		dummymp.process_until_done()
		
		char = ""
		
		while True:
			char = screen.getch()
			if char == ord('q'): 
				break
			elif char == curses.KEY_RIGHT:
				if i<8:
					i += -1
					showFOverlayImage(i)
			elif char == curses.KEY_LEFT:
				if i>0:
					i -= -1
					showFOverlayImage(i)
			elif char == curses.KEY_UP:
				if i>3:
					i=i-4
					showFOverlayImage(i)
				else:
					i=i
					showFOverlayImage(i)
			elif char == curses.KEY_DOWN:
				if i < 4:
					i=i+4
					showFOverlayImage(i)
				else:
					i=i
					showFOverlayImage(i)
			elif char == curses.KEY_ENTER:
				return i
	finally:
		terminateCurses()

