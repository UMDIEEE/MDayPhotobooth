#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2015  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import subprocess

def image_negate(filename):
	
	filename_new = filename.split('.')[0] + "_new." + filename.split('.')[1];
	
	subprocess.call(['convert', filename, '-negate', filename_new])
	
	return filename_new
	
def image_sketch(filename):
	
	filename_new = filename.split('.')[0] + "_new." + filename.split('.')[1];
	
	subprocess.call(['convert', filename, '-sketch', '1', filename_new])
	
	return filename_new

def image_colorswap(filename):
	
	filename_new = filename.split('.')[0] + "_new." + filename.split('.')[1];
	
	subprocess.call(['convert', filename, '-spread', '100', filename_new])
	
	return filename_new
	
def image_cartoon(filename):
	
	filename_new = filename.split('.')[0] + "_new." + filename.split('.')[1];
	
	subprocess.call(['convert', filename, '-auto-gamma', filename_new])
	
	return filename_new
	
def image_paint(filename):
	
	filename_new = filename.split('.')[0] + "_new." + filename.split('.')[1];
	
	subprocess.call(['convert', filename, '-paint', '1', filename_new])
	
	return filename_new
	
def image_emboss(filename):
	
	filename_new = filename.split('.')[0] + "_new." + filename.split('.')[1];
	
	subprocess.call(['convert', filename, '-emboss', '5', filename_new])
	
	return filename_new

if __name__ == '__main__':
	image_cartoon('image.jpg')

