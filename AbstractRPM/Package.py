#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: Package.py 38 2010-02-04 16:28:41Z arinquin $

# Authors : Adrien GENTIL, Arnaud RINQUIN

import os
import rpm
import sys

class Package(object):
    """
    This class represents an RPM package. The attributes for a package are :
        - the *file* path
        - Its RPM header
    """

    def __init__ (self, path):
        
        splitedPath = path.rsplit('/', 1)
        
        self._path = path
        self._directoryPath = splitedPath[0]
        self._fileName = splitedPath[1]
        self._pkgName = self._fileName.rsplit('-', 2)[0] 
        ts = rpm.TransactionSet()
        
        # read rpm header
        pkgFd = os.open(self.path, os.O_RDONLY)
        self._header = ts.hdrFromFdno(pkgFd)
        os.close(pkgFd)
    
    @property
    def fileName(self):
        return self._fileName
    
    @property
    def pkgName(self):
        return self._pkgName

    @property
    def directoryPath(self):
        return self._directoryPath

    @property
    def path(self):
        return self._path
    
    @property
    def header(self):
        return self._header

    def __str__(self):
        return "[Package %s]" % self.path


############ Unit tests ##############

def testPackage(path):
    print Package(path)


class PackageFactory(object):
    """
    The PackageFactory creates Package objects from a RPM file path
    """
    
    @staticmethod
    def createPackageFromPaths(paths):
        """
        DESC : create package objects from package filenames
        PARAMS : paths - a list of RPM filenames
        RETURNS : one list of Package objects
        """
	packages = [Package(path) for path in paths]
	return packages


########## MAIN FOR TESTS ###############

if __name__ == "__main__":
    print("*** Test Package class ***")
    if len(sys.argv) < 2:
        print("Usage : %s <rpm_file_path>" % (sys.argv[0],))
        sys.exit(1)
    testPackage(sys.argv[1])
