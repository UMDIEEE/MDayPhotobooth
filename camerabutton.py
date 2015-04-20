# This is code for raspberry pi to take a picture with a button

from time import sleep #library to control speed of project
import picamera #library to use camera with Python
import RPi.GPIO as GPIO #library to use the GPIO pins with Python (looking at Pins 6 and 8 for Ground and GPIO14)

GPIO.setmode(GPIO.BCM)
button = 14
GPIO.setup(button,GPIO.IN, pull_up_down=GPIO.PUD_UO) #setup button input and set high
while True:
  with picamera.PiCamera() as camera:
    camera.resolution = 1920, 1080
    camera.saturation = 50
    camera.brightness = 50
    GPIO.wait_for_edge(button,GPIO.FALLING)
    camera.start_preview()
    sleep(5) 
    camera.capture("/home/pi/Desktop/image.jpg")
    camera.stop_preview()
  

