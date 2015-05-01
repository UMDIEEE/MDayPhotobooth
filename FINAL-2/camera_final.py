# This is code for raspberry pi to take a picture with a button

from time import sleep #library to control speed of project
import picamera #library to use camera with Python
import subprocess
import curses
import dummymp

import camerafx
from mainsupport import *
from framesupport import *
from textmenu import *
import cups

import os

dummymp.set_max_processes(4)

if __name__ == "__main__":
	print("\033[?17;0;0c")
	
	conn = cups.Connection()
	printers = conn.getPrinters()
	printer_name = printers.keys()[0]
	cups.setUser('pi')
	
	exitNow = False
	while True:
		with picamera.PiCamera() as camera:
			camera.resolution = 640, 480
			camera.saturation = 50
			camera.brightness = 50
			
			filtered_images = fetchAndProcessImages(camera)
			
			camera.stop_preview()
			
			pickSideImages(camera, filtered_images, effectByIndex)
			
			# Two commands to hide the screen stuff:
			# fbgrab temp_picture.png
			# ./bgimage temp_picture.png
			camera.stop_preview()
			camera.resolution = 1944, 2592
			camera.capture("nice_image.jpg")
			
			# Frame the pictures!
			#framed_pics = pic_framed("nice_image.jpg")
			#selected_frame_pic = pickFrameImages(framed_pics)
			#new_pic = frame_pic("nice_image.jpg", selected_frame_pic)
			
			# Show the picture
			#subprocess.call(["fbv", "--stretch", "--noinfo", "-s", "10", new_pic])
			subprocess.call(["fbv", "--stretch", "--noinfo", "-s", "10", "nice_image.jpg"])
			
			# Set options
			setOptions("Print!", "Retake Photo", "Exit")
			response = showMenu()
			
			if response == 1:
				# Print!
				conn.printFile(printer_name, os.path.abspath("nice_image.jpg"), "Photo_Booth_Print", { "media": "Custom.4x6in" })
				subprocess.Popen(["/home/pi/MDay2015/bgimage", "Printing.png"])
				sleep(30)
				exitNow = True
			elif response == 2:
				# Redo
				pass
			elif response == 3:
				exitNow = True
		if exitNow:
			break

