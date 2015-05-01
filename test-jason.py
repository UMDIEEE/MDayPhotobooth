import sys
import termios
import os
import pygame

def getkey():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
        new[6][termios.VMIN] = 1
        new[6][termios.VTIME] = 0
        termios.tcsetattr(fd, termios.TCSANOW, new)
        c = None
        try:
                c = os.read(fd, 1)
        finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, old)
        return c

def car():
    while True:
        key = getkey()
        if key == : #Down arrow
            print "Down"
        elif key == 'K_UP': #Up arrow
            print "Up"
        elif key == 'K_LEFT': 
            print "left"
        elif key == 'K_RIGHT': 
            print "Right"
        elif key == 'q': #Quit
            print "That's It"
            break

car()
