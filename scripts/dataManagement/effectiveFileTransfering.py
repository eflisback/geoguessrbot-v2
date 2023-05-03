"""
This script moves files from one directory structure to another, maintaining their organization. It recursively
traverses the source directory and moves each file to the corresponding destination directory.
"""

import os
import shutil


def move_files(src_dir, dest_dir):
    print("Moved file")

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Loop through items in the source directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        # Move the file if it's a file, or recursively move files in the subdirectory if it's a directory
        if os.path.isfile(src_path):
            shutil.move(src_path, dest_path)
        elif os.path.isdir(src_path):
            move_files(src_path, dest_path)


def main():
    dir_a = '../../data/toBeAdded/1000x1000'
    dir_b = '../../data/countries/training/224x224_enhanced'

    # Loop through subdirectories in the source directory
    for sub_dir_name in os.listdir(dir_a):
        src_sub_dir = os.path.join(dir_a, sub_dir_name)
        dest_sub_dir = os.path.join(dir_b, sub_dir_name)

        # Move files from the source subdirectory to the destination subdirectory
        if os.path.isdir(src_sub_dir):
            move_files(src_sub_dir, dest_sub_dir)


main()
