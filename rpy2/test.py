#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  msda.py
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

#import sys
#import os
#from os import listdir
#import csv


import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr

import numpy

import time



def main():

    #-------------------------------------------------------------------------#
    # libraries in R
    #-------------------------------------------------------------------------#
    importr('readMzXmlData')
    importr('MALDIquant')
    importr('MALDIquantForeign')

    start = time.time()


    #-------------------------------------------------------------------------#
    # specify the file and generate peaks in R
    #-------------------------------------------------------------------------#
    filename = 'DENAMIC_Luba_24042015_nepos_16.mzXML'

    rcode = 'filename ="%s"' % (filename) + '\n' + \
"""
xml <- readMzXmlData::readMzXmlFile(filename,
                                    removeMetaData = TRUE)

ms <- lapply(xml, function(x){
    createMassSpectrum(x$spectrum$mass,
                       x$spectrum$intensity,
                       metaData = list(name=x$metaData$file))})

ms_len = length(xml)

pl <- detectPeaks(ms,
                  method="MAD", halfWindowSize=20, SNR=10,
                  mc.cores=4)
"""

    # Run script
    r(rcode)

    #-------------------------------------------------------------------------#
    # Read data back to Python
    #-------------------------------------------------------------------------#

    # Define the pl as the global variable, so that python can access it.
    r_pl = robjects.globalenv['pl']

    # Retension time (sampling slots)
    pl_len = r('ms_len')
    print pl_len

    # slot id to analyze
    sid = 0

    # read from R to Python for specific fields
    mass = r_pl[sid].do_slot("mass")
    intensity = r_pl[sid].do_slot("intensity")


    mass = numpy.array(mass)
    intensity = numpy.array(intensity)

    end = time.time()
    print end - start

    print type(mass)
    print type(intensity)




#    print mass
#    print intensity



    return 0




if __name__ == '__main__':
    main()
