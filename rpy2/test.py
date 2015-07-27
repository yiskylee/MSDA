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

##from rpy2.robjects import StrVector
##from rpy2.robjects import IntVector
##from rpy2.robjects import FloatVector
import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr
#import rpy2.rinterface as ri

#import subprocess

#import rpy2.interactive as r
#import rpy2.interactive.packages
#import numpy as np

def main():
#    r.source("parallel_peakDetection.R")

    importr('readMzXmlData')
    importr('MALDIquant')
    importr('MALDIquantForeign')


#    filename = 'DENAMIC_Luba_24042015_nepos_16.mzXML'
#    rcode = 'filename = paste("%s")' % (filename)


    r('''
filename = "DENAMIC_Luba_24042015_nepos_16.mzXML"
xml <- readMzXmlData::readMzXmlFile(filename,
                                    removeMetaData = TRUE)

ms <- lapply(xml, function(x){
    createMassSpectrum(x$spectrum$mass,
                       x$spectrum$intensity,
                       metaData = list(name=x$metaData$file))})

ms_seq = vector(mode="list", length = length(xml))

if(.Platform$OS.type == "unix")
{

        p1 <- detectPeaks(ms,
                          method="MAD", halfWindowSize=20, SNR=10,
                          mc.cores=4)
}


    '''
    )
#
    r_p1 = robjects.globalenv['p1']

    rlength = r['length']
    print rlength(r_p1)

    print type(r_p1)
    print type(r_p1[0])


    print r_p1[0].do_slot("mass")
    print r_p1[0].do_slot("intensity")
#    print r_p1[0].rx2("mass")

#    rhead = r['head']
#    print rhead(r_p1)

#    A = np.array(list(r_p1))
#    print A[0,]

#    ri.initr()
#    ri.SexpS4(r_p1)

#    plist = list(r_p1)
#    print type(plist)
#    print plist[0].mass

#    print r_filename
#    print r_filename.r_repr()
#
#    r_xml = robjects.globalenv['xml']



#    print type(r_xml)
#    print r_xml
#    print r_xml.r_repr()

#    readMzXmlData = importr("readMzXmlData")
#    readMzXmlData.readMzXmlFile("DENAMIC_Luba_24042015_nepos_16.mzXML",
#                                removeMetaData = TRUE);



#
#    help_doc = utils.help("help")
#    print help_doc[0]
#
#    x = IntVector(range(10))
#    print x
#
#
#
##    str(help_doc)
#
##    help_where = utils.help_search("help")
##    print tuple(help_where)
#
#
#
#    print r
#
#    pi  = r.pi
#    print pi
#    letters = r.letters;
#    print letters
#
#    print r('1+2')
#
#    sqr = r(
#    'function(x) x^2'
#    )
#    print sqr
#
#    print sqr(2)
#
#    ## using pythojn variables in R
#    x = r.rnorm(100)
#    r('hist (%s, xlab="x", main="hist(x)")' % x.r_repr())
#
#
#    ## use R functions
#    plot = r.plot
#    rnorm = r.rnorm
#    plot(rnorm(100), ylab="random")
#
#
#    ## rpy2 vectors
#    res = StrVector(['abc','def'])
#    print res.r_repr()
#
#    res = FloatVector([1.1, 2.2])
#    print res.r_repr()




    return 0

###
#def find_files(folderName, suffix=".csv" ):
#    filenames = listdir(folderName)
#    return [ filename for filename in filenames if filename.endswith( suffix ) ]



if __name__ == '__main__':
    main()
