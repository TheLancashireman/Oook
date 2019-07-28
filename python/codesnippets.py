#!/usr/bin/python

import os
import hashlib

libRoot = "."

config = { }
fieldmap = { }


def checksum(fname):
	hash_sha512 = hashlib.sha512()
	with open(fname, "rb") as fo:
		while True:
			chunk = fo.read(1048576)
			hash_sha512.update(chunk)
			if len(chunk) < 1048576 :
				break
	return hash_sha512.hexdigest()

def test1():
	for dName, sdName, fList in os.walk(libRoot):
		for fileName in fList:
			fullName = os.path.join(dName, fileName)
			print "FILE:", fileName
			print "  LOCATION:", os.path.relpath(dName, libRoot)
			print "  CHECKSUM:", checksum(fullName)

def readlib(fname, func):
	global cfg, fieldmap
	with open(fname, "r") as fo:
		for line in fo:
			line = line.strip()
			fields = line.split('|')
			if fields[0] == 'Cfg':
				config[fields[1]] = fields[2]
			elif fields[0] == 'Hdr':
				i = 0
				for field in fields:
					fieldmap[field] = i
					i += 1
			elif fields[0] in ( 'Doc', 'New', 'Ign' ):
				func(fields)

def verify_file(fields):
	fullpath = '/'.join( (config['Root'], fields[fieldmap['Path']], fields[fieldmap['File']]) )
	hash = checksum(fullpath)
	if hash != fields[fieldmap['Hash']]:
		print "Discrepancy: ", fullpath

def test2():
	readlib('DavesLibrary.oook.csv', verify_file)

test2()
