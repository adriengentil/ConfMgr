#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: confmgr.py 38 2010-02-04 16:28:41Z arinquin $

# Authors : Adrien GENTIL, Arnaud RINQUIN

import sys

from optparse import OptionParser

import create
import install
import verify

def split_args(liiist):
    if liiist == None:
        return
    sp_list = []
    for l in liiist:
        sp_list.extend(l.split(","))

    return sp_list

##### COMMAND LINE PARSER ####

usage = "usage: %prog --create <configuration>\n\
       %prog [-c <confName,...>] [-r <repo,...>] [-f] --install <writeConf> <pkg1 pkg2 ...>\n\
       %prog --verify <confName> [<confName ...>]"

parser = OptionParser(usage=usage)
parser.add_option("--install", action="store_true", dest="install", default=False, help="install an RPM package")
parser.add_option("--create", action="store_true", dest="create", default=False, help="create configuration with associated RPM database")
parser.add_option("--verify", action="store_true", dest="verify", default=False, help="verify that configurations resolve all dependencies")

parser.add_option("--force", "-f", action="store_true", dest="force", default=False, help="force package installation")
parser.add_option("--conf", "-c", action="append", dest="confs", help="add reading configuration")
parser.add_option("--repo", "-r", action="append", dest="repos", help="add repository")

(options, args) = parser.parse_args()

##### INPUT CHECKING ######

# only one of the three options must be set
if not (options.install ^ options.create ^ options.verify) or \
        not (options.install or options.create or options.verify):
    print parser.get_usage()
    sys.exit(1)

# filter options that work only with install
if not options.install and (options.force or options.confs or options.repos):
    print parser.get_usage()
    sys.exit(2)

# create, install and verify takes at least one argument
if (options.create and len(args) != 1) or \
        (options.install and len(args) < 2) or \
        (options.verify and len(args) == 0):
    print parser.get_usage()
    sys.exit(3)

##### EXECUTE #######
if options.install:
    wconf = args[0]
    rconfs = split_args(options.confs)
    repos = split_args(options.repos)
    packages = args[1:]
    install.install(packages, repos, rconfs, "/", wconf, options.force)

if options.create:
    create.create(args[0])

if options.verify:
    verify.verify(args)

