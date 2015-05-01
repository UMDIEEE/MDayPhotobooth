import subprocess
import curses
import dummymp

global screen

def shrink43Image(img_name):
	imgarr = img_name.split('.')
	basename = ".".join(imgarr[:-1])
	ext = imgarr[-1]
	subprocess.check_output(['convert', img_name, '-resize', '177x236', basename+"_new"+"."+ext])

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
	s.wait()

def showOverlayImage(highlightIndex):
	s = subprocess.Popen(["/home/pi/MDay2015/bgimage", "output-"+str(highlightIndex)+".png"])
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

def pickSideImages(images, callback_change):
	for i in xrange(0, len(images)):
		print "Rendering image: %i" % i
		dummymp.run(drawOverlayImage, images, i, "output-"+str(i)+".png")
	
	dummymp.process_until_done()
	
	try:
		initCurses()
		i = 0
		screen.refresh()
		showOverlayImage(i)
		
		trigger = False
		char = ""
		
		while True:
			char = screen.getch()
			if char == ord('q'): 
				break
			elif char == curses.KEY_RIGHT:
				if i<4:
					i += 4
					showOverlayImage(i)
			elif char == curses.KEY_LEFT:
				if i>3:
					i -= 4
					showOverlayImage(i)
			elif char == curses.KEY_UP:
				if i>0:
					i=i-1
					showOverlayImage(i)
				else:
					i=0
					showOverlayImage(i)
			elif char == curses.KEY_DOWN:
				if i < 7:
					i=i+1
					showOverlayImage(i)
				else:
					i=7
					showOverlayImage(i)
			elif char == curses.KEY_ENTER:
				return i
	finally:
		terminateCurses()

def fetchAndProcessImages():
	os.mkdir("temp")
	
