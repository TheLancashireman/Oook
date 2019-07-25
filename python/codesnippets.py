#!/usr/bin/python

import os
import hashlib

libRoot = "."

def checksum(fname):
    hash_sha512 = hashlib.sha512()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            hash_sha512.update(chunk)
    return hash_sha512.hexdigest()

for dName, sdName, fList in os.walk(libRoot):
    for fileName in fList:
        fullName = os.path.join(dName, fileName)
        print "FILE:", fileName
        print "  LOCATION:", os.path.relpath(dName, libRoot)
        print "  CHECKSUM:", checksum(fullName)

