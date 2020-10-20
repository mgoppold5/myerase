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
# Program which writes a random pattern to a disk.
#
# The program can also check the results.
# You can edit the source code to direct the program.
#
# Look no further for a secure erase program.
# If you use gnu operating system software,
# This program will work on your system,
# to erase any disk you want to.
#
# Erasing a whole disk using a ramdom file,
# is pretty reliable for a secure erasure.
# But, if that's not enough, make a second random file,
# make a second version of "write1.py",
# reconfigure the code, and run it again.
#

import os

k = 1024
m = 1024 * 1024
g = 1024 * 1024 * 1024

OP_WRITE = 1
OP_CHECK = 2

def loadRandom():
	global randBuf
	global RAND_SIZE
	global RAND_FILE

	randBuf = None

	randBuf2 = b""
	f1 = open(RAND_FILE, "rb")
	readSpan = f1.read()
	while(readSpan != 0 and len(readSpan) > 0):
		randBuf2 += readSpan
		readSpan = f1.read()

	if(len(randBuf2) != RAND_SIZE):
		raise Exception("Random buffer size error")

	randBuf = randBuf2

def bufRange(sourceBuf, start, length):
	buf = sourceBuf[start:(start + length)]
	if(len(buf) != length):
		raise Exception("range buf not correct size")
	return buf

def writeOp(f, sourceBuf):
	f.write(sourceBuf)
	return False

def checkOp(f, sourceBuf):
	i = 0
	length = len(sourceBuf)

	buf = f.read(length)
	if(len(buf) != length):
		raise Exception("Buffer that was read, is not the correct size")

	return not (sourceBuf == buf)

def reportReset():
	global reportStr
	global reportSum
	global reportSumPrev
	global reportWasDiff
	
	reportSum = 0
	reportSumPrev = 0
	reportWasDiff = False
	reportStr = ""

def report(diff, progressIndex):
	global reportStr
	global reportSum
	global reportSumPrev
	global reportWasDiff

	if(diff):
		reportWasDiff = True

	while(progressIndex >= reportSum + 128*1024*1024):
		reportSum += 128*1024*1024
		if(reportWasDiff): reportStr += "1 "
		if(not reportWasDiff): reportStr += "0 "
		reportWasDiff = False
		
		if(reportSum >= reportSumPrev + 1024*1024*1024):
			reportSumPrev += 1024*1024*1024
			print(reportStr + "  " + str(reportSumPrev*1.0/g))
			reportStr = ""


def reportFinish(progressIndex):
	global reportStr
	global reportSum
	global reportWasDiff
	
	if(progressIndex > reportSum):
		if(reportWasDiff): reportStr += "1 "
		if(not reportWasDiff): reportStr += "0 "
		reportWasDiff = False
	
	print(reportStr)

def bufOp(f, sourceBuf, start, spanLen, op):
	reportReset()

	sourceSize = len(sourceBuf)

	f.seek(start, os.SEEK_SET);

	writtenLen = 0

	while(True):
		if(writtenLen > spanLen):
			raise Exception("Wrote too many bytes")
		if(writtenLen == spanLen):
			break

		pos = start + writtenLen
		off = pos
		while(off >= sourceSize): off -= sourceSize

		if(off == 0 and ((writtenLen + sourceSize) <= spanLen)):
			if(op == OP_WRITE):
				report(writeOp(f, sourceBuf), writtenLen)
			if(op == OP_CHECK):
				report(checkOp(f, sourceBuf), writtenLen)
			writtenLen += sourceSize
			#print("HEY1")
			continue
	
		thisWriteLen = spanLen - writtenLen
		if(thisWriteLen > sourceSize): thisWriteLen = sourceSize
		if(off + thisWriteLen > sourceSize): thisWriteLen = sourceSize - off

		rBuf = bufRange(sourceBuf, off, thisWriteLen)
		if(op == OP_WRITE):
			report(writeOp(f, rBuf), writtenLen)
		if(op == OP_CHECK):
			report(checkOp(f, rBuf), writtenLen)
		writtenLen += thisWriteLen
		continue

	reportFinish(writtenLen)
	return False

def testCalcNum():
	pass
	#print(m + 931*g + 536280*k + m)
	#print(m + 149*g + 51032*k + m)
	#print(m + 298*g + 93528*k + m)

def showLen(f):
	f.seek(0, os.SEEK_END);
	endPos = f.tell();
	print(endPos)
	pos2 = endPos - 2 * m
	gCount = int(pos2 / g)
	pos2 -= gCount*g
	kCount = pos2 / k
	print("g=" + str(gCount) + " k=" + str(kCount))


def main():
	global randBuf
	global RAND_SIZE
	global RAND_FILE

	RAND_SIZE = 1942838
	RAND_FILE = "random.dat"

	loadRandom()

	if(False):
		print("---------------- disk kingston sa400")
		f = open("/dev/disk/by-id/ata-KINGSTON_SA40088888888_88888888", "r+b")
		showLen(f)
		bufOp(f, randBuf, 0, m + (111)*g + (826840)*k + m, OP_CHECK)
		f.close()

	if(False):
		print("---------------- disk kingston suv400")
		f = open("/dev/disk/by-id/ata-KINGSTON_SUV4008888_88888888", "r+b")
		showLen(f)
		bufOp(f, randBuf, 0, m + (111)*g + (826840)*k + m, OP_CHECK)
		f.close()

	if(False):
		print("---------------- disk sandisk extreme aa01")
		f = open("/dev/disk/by-id/usb-SanDisk_Extreme_AA01888888-0:0", "r+b")
		showLen(f)
		bufOp(f, randBuf, 0, m + (29)*g + (260096)*k + m, OP_CHECK)
		f.close()

main()

