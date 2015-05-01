import os
import subprocess
import curses
import dummymp
import shutil
from camerafx import *

global screen

def shrink43Image(img_name):
	imgarr = img_name.split('.')
	basename = ".".join(imgarr[:-1])
	ext = imgarr[-1]
	newfn = basename+"_new"+"."+ext
	s = subprocess.Popen(['convert', img_name, '-resize', '177x236', newfn])
	s.communicate()
	return newfn

def drawOverlayImage(images, highlightIndex, output_file):
	initialArgs = ['convert', '-size', '1920x1080', 'xc:black']
	curIndex = 0
	
	addlArgs = []
	xOffset = 0
	yOffset = 0
	for image in images:
		if curIndex > 3:
			xOffset = 1682
			yOffset = -270 * 4
		if curIndex == highlightIndex:
			sizing_output = subprocess.check_output(['identify', image])
			sizing_arr = [ int(j) for j in sizing_output.split(" ")[2].split('x') ]
			rectangleArg = "rectangle %i,%i,%i,%i" % (xOffset, (270 * curIndex) + yOffset, xOffset + sizing_arr[0]+4, (270 * curIndex) + sizing_arr[1]+4 + yOffset)
			#rectangleArg = "rectangle %i,%i,%i,%i" % (0, (270 * curIndex), 238, (270 * (curIndex + 1)))
			addlArgs += [ '-fill', 'red', '-draw', rectangleArg ]
		geoArg = "+%i+%i" % (xOffset + 2, (2 + (270 * curIndex)) + yOffset)
		addlArgs += [ image, '-geometry', geoArg, "-composite" ]
		curIndex += 1
	addlArgs += [ output_file ]
	#print(str(initialArgs + addlArgs))
	s = subprocess.Popen(initialArgs + addlArgs)
	s.communicate()

def showOverlayImage(highlightIndex):
	s = subprocess.Popen(["/home/pi/MDay2015/bgimage", "temp/output-"+str(highlightIndex)+".png"])
	s.communicate()

def initCurses():
	global screen
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	screen.keypad(True)
	curses.curs_set(0)
	screen.clear()

def terminateCurses():
	global screen
	curses.nocbreak(); screen.keypad(0); curses.echo()
	curses.endwin()

def processImages(images):
	for i in range(0, len(images)):
		#dummymp.run(drawOverlayImage, images, i, "temp/output-"+str(i)+".png")
		drawOverlayImage(images, i, "temp/output-"+str(i)+".png")
		
	#dummymp.process_until_done()

def refreshScreen():
	global screen
	screen.refresh()

def getScreenChar():
	global screen
	return screen.getch()

def pickSideImages(camera, images, callback_change):
	global screen
	
	try:
		initCurses()
		screen.refresh()
		subprocess.Popen(["/home/pi/MDay2015/bgimage", "Loading.png"])
		processImages(images)
		camera.start_preview()
		i = 0
		screen.refresh()
		showOverlayImage(i)
		
		char = ""
		
		while True:
			char = screen.getch()
			if char == ord(' '): 
				break
			elif char == curses.KEY_RIGHT:
				if i<4 and i+4 < 7:
					i += 4
					showOverlayImage(i)
					if callback_change:
						callback_change(camera, i)
			elif char == curses.KEY_LEFT:
				if i>3:
					i -= 4
					showOverlayImage(i)
					if callback_change:
						callback_change(camera, i)
			elif char == curses.KEY_UP:
				if i>0:
					i=i-1
					showOverlayImage(i)
					if callback_change:
						callback_change(camera, i)
				else:
					i=0
					showOverlayImage(i)
					if callback_change:
						callback_change(camera, i)
			elif char == curses.KEY_DOWN:
				if i < 6:
					i=i+1
					showOverlayImage(i)
					if callback_change:
						callback_change(camera, i)
				else:
					i=6
					showOverlayImage(i)
					if callback_change:
						callback_change(camera, i)
	finally:
		terminateCurses()

def fetchAndProcessImages(camera):
	try:
		shutil.rmtree("temp")
		os.mkdir("temp")
	except:
		pass
	
	subprocess.Popen(["/home/pi/MDay2015/bgimage", "Loading.png"])
	
	imgs = [ "temp/camera_none.jpg", "temp/camera_negative.jpg",
			"temp/camera_sketch.jpg", "temp/camera_colorswap.jpg",
			"temp/camera_cartoon.jpg", "temp/camera_oilpaint.jpg",
			"temp/camera_emboss.jpg" ]
	
	new_imgs = []
		
	camera_effect(camera, 'none')
	camera.capture("temp/camera_none.jpg", use_video_port=True)
	
	camera_effect(camera, 'negative')
	camera.capture("temp/camera_negative.jpg", use_video_port=True)
	
	camera_effect(camera, 'sketch')
	camera.capture("temp/camera_sketch.jpg", use_video_port=True)
	
	camera_effect(camera, 'colorswap')
	camera.capture("temp/camera_colorswap.jpg", use_video_port=True)
	
	camera_effect(camera, 'cartoon')
	camera.capture("temp/camera_cartoon.jpg", use_video_port=True)
	
	camera_effect(camera, 'oilpaint')
	camera.capture("temp/camera_oilpaint.jpg", use_video_port=True)
	
	camera_effect(camera, 'emboss')
	camera.capture("temp/camera_emboss.jpg", use_video_port=True)
	
	for image in imgs:
		new_imgs.append(shrink43Image(image))
	
	camera_effect(camera, 'none')
	
	return new_imgs

def effectByIndex(camera, index):
	camera_effect(camera, [ 'none', 'negative', 'sketch', 'colorswap', 'cartoon',
			'oilpaint', 'emboss' ][index])

