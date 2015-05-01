# This is code for raspberry pi to take a picture with a button

from time import sleep #library to control speed of project
import picamera #library to use camera with Python
import RPi.GPIO as GPIO #library to use the GPIO pins with Python (looking at Pins 6 and 8 for Ground and GPIO14)
import subprocess

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

