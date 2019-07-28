#!/usr/bin/python
#
# Oook - the librarian
#
# (c) David Haworth
#
# This file (Oook.py) is part of Oook
#
# Oook is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Oook is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Oook.  If not, see <http://www.gnu.org/licenses/>.


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
