import subprocess
from mainsupport import *

def frame_pic(pic,frame):
	name = pic.split('.')
	frame_b = frame.split('/')[-1].split('.')[0]
	output= name[0]+'_'+frame_b+'.jpg'
	subprocess.call( ['composite', '-compose', 'atop', '-gravity', 'center', frame, pic, output] )
	return output

def pic_framed(pic):
	frames = [ 'frames/Frame1.png', 'frames/Frame2.png', 'frames/Frame3.png',
				'frames/Frame4.png', 'frames/Frame5.png', 'frames/Frame6.png',
				'frames/Frame7.png' ]
	subprocess.Popen(["/home/pi/MDay2015/bgimage", "Loading.png"])
		
	pics = [pic]
	for frame in frames:
		name = frame.split('.')
		frame_b = frame.split('/')[-1].split('.')[0]
		output= name[0]+'_'+frame_b+'.jpg'
		
		#pics.append(frame_pic(pic, frame))
		
		dummymp.run(frame_pic, str(pic), str(frame))
		pics.append(output)
	
	dummymp.process_until_done()
	
	minipics = []
	
	for picthing in pics:
		imgarr = picthing.split('.')
		basename = ".".join(imgarr[:-1])
		ext = imgarr[-1]
		newfn = basename+"_new"+"."+ext
		
		#minipics.append(shrink43Image(picthing))
		minipics.append(newfn)
		dummymp.run(shrink43Image, str(picthing))
	
	dummymp.process_until_done()
	
	return minipics

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
	global screen
	try:
		initCurses()
		subprocess.Popen(["/home/pi/MDay2015/bgimage", "Loading.png"])
		i = 0
		refreshScreen()
		
		for i in xrange(0, len(images)):
			#drawFOverlayImage(images, i, "temp/output-frame-"+str(i)+".png")
			dummymp.run(drawFOverlayImage, [x for x in images], int(i), str("temp/output-frame-"+str(i)+".png"))
		
		dummymp.process_until_done()
		
		showFOverlayImage(i)
		
		char = ""
		
		while True:
			char = getScreenChar()
			if char == ord(' '): 
				break
			elif char == curses.KEY_RIGHT:
				if i<7:
					i += 1
					showFOverlayImage(i)
				else:
					i = 7
					showFOverlayImage(i)
			elif char == curses.KEY_LEFT:
				if i>0:
					i -= 1
					showFOverlayImage(i)
				else:
					i = 0
					showFOverlayImage(i)
			elif char == curses.KEY_UP:
				if i>3:
					i=i-4
					showFOverlayImage(i)
			elif char == curses.KEY_DOWN:
				if i < 4 and i+4 < 7:
					i=i+4
					showFOverlayImage(i)
	finally:
		terminateCurses()
	return images[i]
