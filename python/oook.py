#!/usr/bin/python
#
# Oook - the librarian
#
# (c) David Haworth
#
# This file (oook.py) is part of Oook
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
import sys
import hashlib

# Global variables
config = { }
fieldmap = { }

def main():
	if not os.access(sys.argv[2], os.R_OK):
		print 'Cannot access', sys.argv[2]
		usage()
		exit(1)
	if sys.argv[1] == 'verify':
		verify_library(sys.argv[2])
		process_lib(sys.argv[2], verify_file)
	else:
		print 'Unknown command ', sys.argv[1]
		usage()
		exit(1)

def usage():
	print 'Usage: oook <command> <oook-file> [options]'

def verify_library(lname):
	process_lib(lname, verify_file)

def process_lib(fname, func):
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
	if os.access(fullpath, os.R_OK):
		hash = hash_file(fullpath)
		if hash != fields[fieldmap['Hash']]:
			print "Hash discrepancy: ", fullpath
	else:
		print "Missing file: ", fullpath

def hash_file(fname):
	hash_sha512 = hashlib.sha512()
	with open(fname, "rb") as fo:
		while True:
			chunk = fo.read(1048576)
			hash_sha512.update(chunk)
			if len(chunk) < 1048576 :
				break
	return hash_sha512.hexdigest()

main()
