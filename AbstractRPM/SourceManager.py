#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: SourceManager.py 38 2010-02-04 16:28:41Z arinquin $

# Authors : Adrien GENTIL, Arnaud RINQUIN

import rpm
import os
import re
import sys

from Utils import GlobDirectoryWalker
from Package import PackageFactory

class SourceManager(object):

    _packages = []

    @staticmethod
    def loadPaths (paths):
        """
        DESC : load packages and services from each source urls
        PARAMS : paths - repository list
        RETURNS :
        """
        if paths == None:
            return

        for path in paths:
            SourceManager._packages.extend(PackageFactory.createPackageFromPaths( GlobDirectoryWalker(path,"*.rpm")))
    
    @staticmethod
    def findPackages(packageNameOrPath):
        """
        DESC : find packages in repository
        PARAMS : packageNameOrPath - package name or path to a package
        RETURNS : matching packages
        """
        p = re.compile(".*"+ packageNameOrPath +".*", re.IGNORECASE) 
        matchingPackages = []
        for package in SourceManager._packages:
            if package.fileName == packageNameOrPath or package.path == packageNameOrPath or p.match(package.pkgName):
                matchingPackages.append(package)
        return matchingPackages

    def __str__(self):	
        return "%s available packages %s" % (len(SourceManager._packages), [str(p) for p in SourceManager._packages])

############ Unit tests ##############

def testSourceManager():
    if len(sys.argv) < 3:
        print("Usage : %s <package_name> <directory_path_1, directory_path_2>" % (sys.argv[0],))
        sys.exit(1)

    paths = sys.argv[2:]
    print "SourceManager loads paths %s" % paths

    SourceManager.loadPaths(paths)
    print SourceManager()

def testFindPackage():
    packages = SourceManager.findPackages(sys.argv[1])
    print "Found %s paths for package %s : %s" % (len(packages), sys.argv[1], [str(p.fileName) for p in packages])  

########## MAIN FOR TESTS ###############

if __name__ == "__main__":
    print("*** Test SourceManager class ***")
    testSourceManager()

    print("*** Test findPackage ***")
    testFindPackage()
        
