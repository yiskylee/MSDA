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

import sys
import os
#from os import listdir
#import csv
#from rpy2.robjects import r
import subprocess

def main():

    if len(sys.argv) == 1:
        print "Please specify the csv file folder."
        sys.exit()

    if len(sys.argv) > 2:
        print "Too many arguments."
        sys.exit()

    file_dir = sys.argv[1]
#    print file_dir

    for root, dirs, files in os.walk(file_dir, topdown=False):
        for name in files:
            if name.endswith(".csv"):
                file_name = os.path.join(root, name)
                rscript = "./sample.R " + file_name
                subprocess.check_call([rscript], shell = True)

#    filenames = find_files(folderName, suffix = ".csv")
#    for name in filenames:
#        print name



    return 0

###
#def find_files(folderName, suffix=".csv" ):
#    filenames = listdir(folderName)
#    return [ filename for filename in filenames if filename.endswith( suffix ) ]



if __name__ == '__main__':
    main()
