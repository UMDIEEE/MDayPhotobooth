import subprocess
import curses
import dummymp
from mainsupport import *

def showMenu():
	i=1
	try:
		initCurses()
		refreshScreen()
		run(i)
		while True:
			char = getScreenChar()
			if char == ord(' '): 
				break
			elif char == curses.KEY_RIGHT:
				pass
			elif char == curses.KEY_LEFT:
				pass
			elif char == curses.KEY_UP:
				if i>1:
					i=i-1
					run(i)
				else:
					i=1
					run(i)
			elif char == curses.KEY_DOWN:
				if i < 3:
					i=i+1
					run(i)
				else:
					i=3
					run(i)
	finally:
		terminateCurses()
	return i
def run(num):	
	if num==1:
		subprocess.call(['/home/pi/MDay2015/bgimage','new-jason-menu1.png'])
	elif num==2:
		subprocess.call(['/home/pi/MDay2015/bgimage','new-jason-menu2.png'])
	elif num==3:
		subprocess.call(['/home/pi/MDay2015/bgimage','new-jason-menu3.png'])

def setOptions(in1,in2,in3):
	Option1="text 0,-200 '"+in1+"'"
	Option2="text 0,0 '" +in2+"'"
	Option3="text 0,200 '"+in3+"'"
	subprocess.Popen(["/home/pi/MDay2015/bgimage", "Loading.png"])
	dummymp.run(subprocess.call,['convert', '-size', '1920x1080' ,'xc:gray' ,'-gravity', 'Center', '-pointsize' ,'48' ,'-fill',
	 'blue', '-draw',"text 0,-400 'What would you like to do?'",'-fill','red','-draw',"rectangle 760,300 1160,400",
	  '-pointsize' ,'35' ,'-fill' ,'black','-draw' ,Option1, '-draw' ,Option2, '-draw' ,Option3, 'new-jason-menu1.png'])
	dummymp.run(subprocess.call,['convert', '-size', '1920x1080' ,'xc:gray' ,'-gravity', 'Center', '-pointsize' ,'48' ,'-fill',
	 'blue', '-draw',"text 0,-400 'What would you like to do?'", '-pointsize' ,'35' ,'-fill' ,'black' ,'-draw' ,Option1,
	 '-fill','red','-draw',"rectangle 760,500 1160,600",'-fill','black','-draw' ,Option2, '-draw' ,Option3, 'new-jason-menu2.png'])
	dummymp.run(subprocess.call,['convert', '-size', '1920x1080' ,'xc:gray' ,'-gravity', 'Center', '-pointsize' ,'48' ,'-fill',
	 'blue', '-draw',"text 0,-400 'What would you like to do?'", '-pointsize' ,'35' ,'-fill' ,'black' ,'-draw' ,Option1,
	  '-draw' ,Option2,'-fill','red','-draw',"rectangle 760,700 1160,800",'-fill','black','-draw' ,Option3, 'new-jason-menu3.png'])
	dummymp.process_until_done()

