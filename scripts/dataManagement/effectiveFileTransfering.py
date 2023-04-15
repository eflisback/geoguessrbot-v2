import os
import shutil


def move_files(src_dir, dest_dir):
    print("Moved file")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            shutil.move(src_path, dest_path)
        elif os.path.isdir(src_path):
            move_files(src_path, dest_path)


def main():
    dir_a = '../../data/toBeAdded/1000x1000'
    dir_b = '../../data/training/224x224_enhanced'

    for sub_dir_name in os.listdir(dir_a):
        src_sub_dir = os.path.join(dir_a, sub_dir_name)
        dest_sub_dir = os.path.join(dir_b, sub_dir_name)

        if os.path.isdir(src_sub_dir):
            move_files(src_sub_dir, dest_sub_dir)


main()
