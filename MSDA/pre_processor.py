import numpy as np
import pandas as pd

# Generate even or odd scans (lc-ms or hcd)
import sys
import os


def gen_partial_scans(input_file_paths, output_dir, even_or_odd, lower, upper):
    for input_file_path in input_file_paths:
        all_scan_df = pd.read_csv(input_file_path)
        # To deal with euro samples whose scan_id column has a format of
        # "140716_DENAMIC_MADRES_NEG_21-1"
        if all_scan_df.ix[:, 0].dtype != np.int64:
            all_scan_df.ix[:, 0] = \
                all_scan_df.ix[:, 0].apply(lambda x: int(x.split('-')[1]))
        all_scan = all_scan_df.as_matrix()
        scan_num = all_scan[:, 0]
        if even_or_odd == 'even':
            selection = \
                np.logical_and(np.logical_and(scan_num >= lower, scan_num <= upper),
                               scan_num % 2 == 0)
        elif even_or_odd == 'odd':
            selection = \
                np.logical_and(np.logical_and(scan_num >= lower, scan_num <= upper),
                               scan_num % 2 == 1)
        elif even_or_odd == 'pos':
            selection = \
                np.logical_and(np.logical_and(scan_num >= lower, scan_num <= upper),
                               scan_num % 4 == 0)
        elif even_or_odd == 'neg':
            selection = \
                np.logical_and(np.logical_and(scan_num >= lower, scan_num <= upper),
                               scan_num % 4 == 2)
        else:
            print 'Tell me which kind of scans (even / odd / neg / pos) are needed'
            sys.exit(-1)
        input_file_name = input_file_path.split('/')[-1]
        output_file_path = os.path.join(output_dir, input_file_name)
        print output_file_path
        np.savetxt(output_file_path, all_scan[selection], delimiter=',')