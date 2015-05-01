# This is code for raspberry pi to take a picture with a button

from time import sleep #library to control speed of project
import picamera #library to use camera with Python
import RPi.GPIO as GPIO #library to use the GPIO pins with Python (looking at Pins 6 and 8 for Ground and GPIO14)
import subprocess

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
			xOffset = -1920
			yOffset = 540
		if curIndex == highlightIndex:
			sizing_output = subprocess.check_output(['identify', image])
			sizing_arr = [ int(j) for j in sizing_output.split(" ")[2].split('x') ]
			rectangleArg = "rectangle %i,%i,%i,%i" % ((480 * curIndex) + xOffset, yOffset, xOffset + (480 * curIndex) + sizing_arr[0]+8, sizing_arr[1]+8 + yOffset)
			#rectangleArg = "rectangle %i,%i,%i,%i" % (0, (270 * curIndex), 238, (270 * (curIndex + 1)))
			addlArgs += [ '-fill', 'red', '-draw', rectangleArg ]
		geoArg = "+%i+%i" % (xOffset + 4 + (480 * curIndex), (4 + yOffset))
		addlArgs += [ image, '-geometry', geoArg, "-composite" ]
		curIndex += 1
	addlArgs += [ output_file ]	
	print(str(initialArgs + addlArgs))
	subprocess.check_output(initialArgs + addlArgs)

if __name__ == "__main__":
	print("\033[?17;0;0c")
	
	GPIO.setmode(GPIO.BCM)
	button = 14
	GPIO.setup(button,GPIO.IN, pull_up_down=GPIO.PUD_UP) #setup button input and set high
	while True:
	  with picamera.PiCamera() as camera:
	    camera.resolution = 640, 480
	    camera.saturation = 50
	    camera.brightness = 50
	    #camera.rotation= 90
	    #GPIO.wait_for_edge(button,GPIO.FALLING)
	    camera.start_preview()
	    #sleep(5) 
	    #camera.capture("/home/pi/Desktop/image.jpg")
	    #camera.stop_preview()
	    raw_input()
	    # Two commands to hide the screen stuff:
	    # fbgrab temp_picture.png
	    # ./bgimage temp_picture.png
	    #t = subprocess.check_output(['fbgrab', '/home/pi/MDay2015/temp_picture.png'])
	    camera.capture("/home/pi/MDay2015/temp_picture.jpg", use_video_port=True)
	    t2 = subprocess.check_output(['/home/pi/MDay2015/bgimage', '/home/pi/MDay2015/temp_picture.jpg'])
	    #camera.resolution = 2592, 1944
	    camera.resolution = 1944, 2592
	    camera.capture("/home/pi/Desktop/image.jpg")
	print("\033[0m")

