#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: install.py 38 2010-02-04 16:28:41Z arinquin $

# Authors : Adrien GENTIL, Arnaud RINQUIN

import rpm
import os
import sys

import utils
from AbstractRPM.Package import PackageFactory
from AbstractRPM.SourceManager import SourceManager
from AbstractRPM.Configurations import ConfigurationManager

rpmtsCallback_fd = None

def install(packageNames, sourcePaths, readConfsPaths, refConfPath, writeConfPath, forced = False):

    SourceManager.loadPaths(sourcePaths)
    packagesToInstall = []
    install = True
    
    for packageName in packageNames:
        possiblePackages = SourceManager.findPackages(packageName)
        if len(possiblePackages) < 1:
            try:
                fd = os.open(packageName, os.O_RDONLY)
                os.close(fd)
                packagesToInstall.extend(PackageFactory.createPackageFromPaths([packageName]))
            except:
                install = False
                print('Unable to find matching package for name %s' % packageName)
                sys.exit(6)
        elif len(possiblePackages) == 1:
            package = possiblePackages[0]
            packagesToInstall.append(package)
            print('Found unique package matching %s : %s' % (packageName, package.path))
        else:
            print('Several packages match the name %s :' % packageName)
            i = 0
            for possiblePackage in possiblePackages:
                print('[%s]%s' % (i, possiblePackage.path)) 
                i+=1
            while True:
                choice = 0
                var = raw_input('which one do you want to install ? ')
                try:
                    choice = int(var)
                except:
                    print "Invalid input"
                    continue
                if choice > -1 and choice < len(possiblePackages):
                    package = possiblePackages[choice]
                    packagesToInstall.append(package)  
                    print('%s selected' % package.path)                    
                    break
                else:
                    print("Input out of range")
    
    # if error on given package(s) has occurred, do nothing
    if install == False:
        return
    
    headers = [package.header for package in packagesToInstall]

    ConfigurationManager.loadConfigurations(readConfsPaths, refConfPath, writeConfPath)
    
    dependencies = ConfigurationManager.verifyForInstall(headers)
    if len(dependencies) > 0:
        print "Dependencies cannot be resolved :"
        for r in dependencies:
            print("%s" % (utils.printHeaders(r), ))
        if forced:
            print "Forcing installation..."
        else:
            return

    ConfigurationManager.install([package.path for package in packagesToInstall])
    print "Installed packages : ", [package.path for package in packagesToInstall]
