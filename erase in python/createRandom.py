#
# Copyright (c) 2019 Mike Goppold von Lobsdorf
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

#
# Program which creates a file with random zeros and ones.
#

import os
import random
import struct

def randomCharacter():
	#numLimit = 6
	numLimit = 256

	c = random.random() * numLimit
	c = int(c)
	if(c == numLimit): c -= 1
	return c

def main():
	targetLen = 1024 * 1024
	targetLen += int(random.random() * 1024 * 1024)

	s = b""

	while(True):
		needToAdd = targetLen - len(s)
		randomAddition = b""
		if(needToAdd == 0): break

		while(True):
			if(len(randomAddition) + 1 > needToAdd): break
			if(len(randomAddition) > 256): break
			randomAddition += struct.pack('B', randomCharacter())
		
		s += randomAddition

	print(len(s))
	
	fName = "random.dat"

	if(os.path.isfile(fName)):
		#os.system("del /y " + fName)
		os.system("rm " + fName)

	f = open(fName, "wb")
	f.write(s)

main()

