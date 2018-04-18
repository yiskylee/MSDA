import os
import re
import pandas as pd


def find_files_with_regex(base_dir, file_pattern):
    file_paths = [os.path.abspath(os.path.join(root, file_name))
                  for root, dirs, files in os.walk(base_dir)
                  for file_name in files if re.match(file_pattern, file_name)]
    return file_paths

def combine_tables():
    table1 = pd.read_excel('/mnt/data/PROTECT/spain_60/meta/Correlation samples and raw data files names.xls')
    table2 = pd.read_excel('/mnt/data/PROTECT/spain_60/meta/Protect_Analysis Key for SpainRoger 60.xlsx')
    table = table1.merge(table2, left_on='Sample Name', right_on='Sample')
    table[['Raw File Name', 'Sample Name', 'Birth Outcome']].\
        to_csv('/mnt/data/PROTECT/spain_60/meta/labels.csv', index=False)