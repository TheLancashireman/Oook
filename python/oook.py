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
db = [ ]

# main()
#
# The main function. The script body (at the end) does nothing but call this function
def main():
	if not os.access(sys.argv[2], os.R_OK):
		print 'Cannot access', sys.argv[2]
		usage()
		exit(1)
	if sys.argv[1] == 'verify':
		# Verify all files in database
		verify_library(sys.argv[2])
	elif sys.argv[1] == 'scan':
		# scan the directory tree for unrecorded files
		scan_root(sys.argv[2])
	else:
		print 'Unknown command ', sys.argv[1]
		usage()
		exit(1)

def usage():
	print 'Usage: oook <command> <oook-file> [options]'

# verify_library()
#
# Command = verify
# Verify all file records in the database. Report missing and changed files
def verify_library(lname):
	# No need to read the DB into memory first. Process it on the fly
	process_db(lname, verify_file)

# scan_root()
#
# Command = scan
# Scan the library's directory (starting at the root) and report all new files
def scan_root(lname):
	# Read the database into memory first
	load_db(lname)
	# Now scan the root directory for files
	for dName, sdList, fList in os.walk(config['Root']):
		for filename in fList:
			relpath = os.path.relpath(dName, config['Root'])
			if not is_file_in_db(filename, relpath):
				print_new_file(relpath, filename)

# load_db()
#
# Load the database into memory
# The database is stored as an array of arrays
def load_db(lname):
	process_db(lname, append_record)

# process_db()
#
# Process the library database. Store the configuration, call specified function for each file
def process_db(fname, func):
	global cfg, fieldmap, nfields
	with open(fname, "r") as fo:
		for line in fo:
			line = line.strip()
			fields = line.split('|')
			if fields[0] == 'Cfg':
				config[fields[1]] = fields[2]
			elif fields[0] == 'Hdr':
				nfields = 0
				for field in fields:
					fieldmap[field] = nfields
					nfields += 1
			elif fields[0] in ( 'Doc', 'New', 'Ign' ):
				func(fields)

# is_file_in_db()
#
# Returns True if relpath/file combination is in the db
def is_file_in_db(fname, relpath):
	global db
	print 'Looking for ', relpath, '/', fname
	path_idx = fieldmap['Path']
	file_idx = fieldmap['File']
	for rec in db:
		if rec[file_idx] == fname and rec[path_idx] == relpath:
			return True
	return False
	

# verify_file()
#
# Verify as single file record in the DB.
# The DB fields are passed as parameters
def verify_file(fields):
	global config, fieldmap
	fullpath = os.path.join(os.path.join(config['Root'], fields[fieldmap['Path']]), fields[fieldmap['File']])
	if os.access(fullpath, os.R_OK):
		hash = hash_file(fullpath)
		if hash != fields[fieldmap['Hash']]:
			print "Hash discrepancy: ", fullpath
	else:
		print "Missing file: ", fullpath

# append_record()
#
# Append a single record from the database to the internal db storage
def append_record(fields):
	global db
	db.append(fields)

	return ''

# hash_file()
#
# Compute a hash of the specified file. Currently fixed as sha512, but could be made selectable (see Cfg|Hash)
def hash_file(fname):
	hash_sha512 = hashlib.sha512()
	with open(fname, "rb") as fo:
		while True:
			chunk = fo.read(1048576)
			if len(chunk) == 0:
				# End of file: don't pass an empty chunk to the hash computation (not sure what happens)
				break
			hash_sha512.update(chunk)
			if len(chunk) < 1048576:
				# End of file reached
				break
	return hash_sha512.hexdigest()

# is_file_in_db()
#
# Search the db for a given path/file and return True if found
def is_file_in_db(fname, pname):
	for record in db:
		if (record[fieldmap['File']] == fname) and (record[fieldmap['Path']] == pname):
			return True
	return False

# print_new_file()
#
# Print a line in DB format for a new file
def print_new_file(relpath, filename):
	global config, fieldmap
	if relpath == '.':
		relpath = ''
		fullpath = os.path.join(config['Root'], filename)
	else:
		fullpath = os.path.join(os.path.join(config['Root'], relpath), filename)
	if os.access(fullpath, os.R_OK):
		hash = hash_file(fullpath)
	else:
		hash = "FILE_UNREADABLE"
	line = []
	i = 0
	while i < nfields:
		line.append('')
		i += 1
	line[0] = "New"
	line[fieldmap['Path']] = relpath
	line[fieldmap['File']] = filename
	line[fieldmap['Hash']] = hash
	print '|'.join(line)

# The script body - just call main()
main()
