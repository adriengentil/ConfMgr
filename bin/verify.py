#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: verify.py 38 2010-02-04 16:28:41Z arinquin $

# Authors : Adrien GENTIL, Arnaud RINQUIN

import utils
from AbstractRPM.Configurations import ConfigurationManager as CM


def verify(confPaths):
    CM.loadConfigurations(confPaths, '/')
    requires = CM.verify()

    if len(requires) == 0:
        print("All dependencies resolved")
    else:
        print("These dependencies cannot be resolved :")
        for r in requires:
            print("%s" % (utils.printHeaders(r), ))

