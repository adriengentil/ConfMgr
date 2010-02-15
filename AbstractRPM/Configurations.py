#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: Configurations.py 38 2010-02-04 16:28:41Z arinquin $

# Authors : Adrien GENTIL, Arnaud RINQUIN

import os
import rpm

class ConfigurationManager(object):
    """
    ConfigurationManager manage a set of configuration 
    """
    
    _hdrs = []
    _confs = []
    _refConf = None
    _writeConf = None

    @staticmethod
    def loadConfigurations(readConfPaths, refConfPath, writeConfPath = None):
        """
        DESC : load configurations in the manager
        PARAMS : readConfPaths - paths to the reading configurations
                 refConfPath - paths to the reference configuration, the dependencies are resolved on this conf
                 writeConfPath - configuration where the RPM packages are installed
        """
        if readConfPaths == None:
            readConfPaths = []
        
        ConfigurationManager._refConf = Configuration(refConfPath, False)
        
        if writeConfPath == None:
            ConfigurationManager._confs, ConfigurationManager._hdrs = ConfigurationManager._parseHdrInConfs(readConfPaths)
        else:
            readConfPaths.insert(0, writeConfPath)
            ConfigurationManager._confs, ConfigurationManager._hdrs = ConfigurationManager._parseHdrInConfs(readConfPaths)
            ConfigurationManager._writeConf = ConfigurationManager._confs[0]

    @staticmethod
    def _parseHdrInConfs(confPaths):
        """
        DESC : create conf objects and extracts headers from installed packages in each confs
        PARAMS : - confPaths list of configuration paths
        RETURNS : two lists : Configuration list
                              header list
        """
        hdrs = []
        confs = []
        for confPath in confPaths:
            c = Configuration(confPath)
            confs.append(c)
            hdrs.extend(c.hdrs)
        return confs, hdrs

    @staticmethod
    def install(pkgPaths):
        """
        DESC : install packages in the writeConfPath
        PARAMS : pkgPaths - list of packages paths
        RETURNS :
        """
        #print("Installing packages in conf %s" % ConfigurationManager._writeConf.confPath)
        ConfigurationManager._writeConf.install(pkgPaths)

    @staticmethod
    def verify():
        """
        DESC : compute dependencies resolved between configurations
        PARAMS : 
        RETURNS : the unresolved dependencies
        """
        dep = ConfigurationManager._verify(ConfigurationManager._hdrs)
        return dep

    @staticmethod
    def verifyForInstall(hdrs):
        """
        DESC : compute dependencies resolved between configurations and packages
        PARAMS : hdrs - list of headers
        RETURNS : the unresolved dependencies
        """
        t_hdrs = ConfigurationManager._hdrs[:]
        t_hdrs.extend(hdrs)
        dep = ConfigurationManager._verify(t_hdrs)
        return dep

    @staticmethod
    def _verify(hdrs):
        """
        DESC : compute dependencies on the refConf
        PARAMS : hdrs - list of headers
        RETURNS : the unresolved dependencies
        """
        dep = ConfigurationManager._refConf.checkHeaders(hdrs)
        return dep

    @staticmethod
    def createConf(path):
        """
        DESC : create a configuration
        PARAMS : path - directory where the configuration will be created
        RETURNS :
        """
        if not os.path.isdir(path) and not os.path.isdir(path.rsplit('/', 1)[0]):
            raise Exception(path + ' not a directory')

        RPMdb = path + Configuration.DEFAULT_RPM_DB_PATH
        os.makedirs(RPMdb)
    
        rpm.addMacro("_prefix", path)
        rpm.addMacro("_dbpath", RPMdb)
        ts = rpm.TransactionSet()
        ts.initDB()

class Configuration(object):
    """
    Represents a configuration. A configuration is a set of services with it's
    own RPM database. It's attributes are :
        - path to the configuration
        - default path to the RPM database
        - RPM lib's TransactionSet object
    """

    DEFAULT_RPM_DB_PATH = '/var/lib/rpm'

    def __init__(self, confPath, readHeaders = True, RPMDbPath = DEFAULT_RPM_DB_PATH):
        """
        DESC : Constructor for Configuration class. Two arguments :
        PARAMS : - confPath : configuration path
                 - RPMDbPath : -TESTING ONLY- *relative* RPM database path in the configuration - 
        """
        self._confPath = confPath
        self._RPMDbPath = RPMDbPath
        #rpm.setVerbosity(7)
        rpm.addMacro("_dbpath",  self._confPath + self._RPMDbPath)

        self._ts = rpm.TransactionSet()

        #self._ts.Debug(1)
        self._ts.openDB()
        rpm.delMacro("_dbpath")
        self._hdrs = []
        if readHeaders:
            self._parseHdrs()

    @property
    def RPMDbPath(self):
        return self._RPMDbPath

    @property
    def confPath(self):
        return self._confPath

    @property
    def hdrs(self):
        return self._hdrs

    def _parseHdrs(self):
        """
        DESC : Extracts installed package headers from the RPM DB and creates Service and RequiredService lists
        PARAMS : 
        RETURNS : two lists, the first is the provided services (Service object) and the second is the Required object (RequiredServices object)
        """
        self._hdrs = []

        mi = self._ts.dbMatch()
        for hdr in mi:
            self._hdrs.append(hdr)

    def install(self, pkgPaths):
        """
        DESC : Install package(s) in the configuration
        PARAMS : - packages, package list to be installed
        RETURNS : 
        """
        for pkg in pkgPaths:
            fd = os.open(pkg, os.O_RDONLY)
            hdr = self._ts.hdrFromFdno(fd)
            prefix = hdr[rpm.RPMTAG_PREFIXES][0] if len(hdr[rpm.RPMTAG_PREFIXES]) > 0 else ""
            command = "rpm -Uvh --nodeps --prefix "+ self._confPath + prefix +" --dbpath "+ self._confPath + self._RPMDbPath +" "+ pkg
            os.close(fd)
            os.system(command)
        
    def checkHeaders(self, hdrs):
        """
        DESC : compute dependencies on this conf
        PARAMS : hdrs - headers to verify
        RETURNS : unresolved dependencies
        """
        t_hdrs = self.hdrs[:]
        t_hdrs.extend(hdrs)
        for h in hdrs:
            self._ts.addInstall(h, "")
        
        return self._ts.check()

    def __str__(self):
        return "Configuration path : %s - Configuration RPM DB : %s" % (self.confPath, self.RPMDbPath)

