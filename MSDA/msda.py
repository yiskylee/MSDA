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
import pre_processor
import os
import util
# from os import listdir
# import csv
# from rpy2.robjects import r
import subprocess


def main():
    if len(sys.argv) <= 3:
        print "Usage: python msda.py input_dir output_dir " \
              "file_type(csv or mzXML) [even / odd / neg / pos]"
        sys.exit(-1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    if not os.path.exists(input_dir):
        print "Input directory does not exist, exiting..."
        sys.exit(-1)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_pattern = ".*" + "." + sys.argv[3]
    file_type = sys.argv[3]

    # Converting mzXML to peaklists
    if file_type == "mzXML":
        r_command = "Rscript ./mzxml_to_peaks.R " + input_dir + " " + output_dir
        subprocess.check_call([r_command], shell=True)
    # Converting peaklists to
    elif file_type == "csv":
        if len(sys.argv) != 5:
            print "What kinds of peaks do you want (even / odd / neg / pos)?"
            sys.exit(-1)
        if 'even' not in input_dir or 'odd' not in input_dir:
            print "Now generating LC-MS data from the given peak lists"
            input_file_paths = \
                util.find_files_with_regex(input_dir, file_pattern)
            pre_processor.gen_partial_scans(input_file_paths,\
                                            output_dir, sys.argv[4], 80, 1400)

    return 0

if __name__ == '__main__':
    main()
