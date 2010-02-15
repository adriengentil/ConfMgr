#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: create.py 38 2010-02-04 16:28:41Z arinquin $

# Authors : Adrien GENTIL, Arnaud RINQUIN

import os
import rpm
import sys

from AbstractRPM.Configurations import ConfigurationManager as CM

def create(path):
    #try:
    CM.createConf(path)
    #except:
    #    print "Error:", sys.exc_info()[0]
    #    sys.exit(4)
        
