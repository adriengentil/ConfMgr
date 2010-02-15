#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: utils.py 38 2010-02-04 16:28:41Z arinquin $

# Authors : Adrien GENTIL, Arnaud RINQUIN

import rpm

def printHeaders(hdr):
    str = ""
    i = 0
    flag = hdr[2]
    if flag & rpm.RPMSENSE_LESS:
        str += "<"
        i += 1
    if flag & rpm.RPMSENSE_GREATER:
        str += ">"
        i += 1
    if flag & rpm.RPMSENSE_EQUAL:
        str += "="
        i += 1
    
    str += " " * (3 - i)
    str += hdr[1][0]
    if hdr[1][1] != None:
        str += "-"+ hdr[1][1]
        if hdr[1][2] != None:
            str += "-"+ hdr[1][2]

    return str
