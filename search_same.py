#!/usr/bin/python3

''' 
    USAGE: ./search_same.py --path ./{folder_with_images}/ 
'''

import sys
import os
import math
from PIL import Image, ImageChops
import numpy as np

# With multiprocessing it works 1.5x faster
from multiprocessing.dummy import Pool as ThreadPool


def main(argv):
    ''' Checking if images in folder are similar or duplicates '''

    path = _check_if_valid_path(argv)

    if path:
        files = np.asarray([path + "/" + i for i in os.listdir(path)])

        for i in range(1, len(files) - 1):
            pool = ThreadPool()
            pool.map(lambda f1: rmsdiff(f1, files[i:][0]), files[i:])

            pool.close()
            pool.join()


# Root-Mean-Square Difference 
def rmsdiff(file1: Image, file2: Image):
    ''' Calculate the root-mean-square difference between two images '''

    im1 = Image.open(file1).convert('L').resize((32, 32), resample=Image.BICUBIC)
    im2 = Image.open(file2).convert('L').resize((32, 32), resample=Image.BICUBIC)
                
    diff_hist = ImageChops.difference(im1, im2).histogram()
    sum_of_squares = sum( (value * (idx * idx) for idx, value in enumerate(diff_hist)) )
    rms = np.sqrt(sum_of_squares / float(im1.size[0] * im1.size[1]))

    file1 = file1.split("/")[-1]
    file2 = file2.split("/")[-1]

    if rms <= 41 and file1 != file2: print(f"{file1} <=> {file2}")


def _check_if_valid_path(argv):
    ''' Usage help '''

    if "--path" not in argv:
        print("usage: search_same.py [-h] --path PATH")
        if "--help" not in argv or "-h" not in argv:
            print("search_same.py: error: the following arguments are required: --path")
        else: 
            print("\nFirst test task on images similarity.\noptional arguments:\n" +
                "-h, --help           show this help message and exit\n" +
                "--path PATH          folder with images")
        return None    
    return argv[-1]


if __name__ == "__main__":  
    main(sys.argv[1:])
