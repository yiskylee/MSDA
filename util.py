import os
import re


def find_files_with_regex(base_dir, file_pattern):
    file_paths = [os.path.abspath(os.path.join(root, file_name))
                  for root, dirs, files in os.walk(base_dir)
                  for file_name in files if re.match(file_pattern, file_name)]
    return file_paths
