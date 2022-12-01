# Implementation of the Bravo & Farid scale invariant clutter measure, based on the segmentation of the image (https://doi.org/10.1167/8.1.23)

import argparse
from os import listdir
from os.path import isfile, join, abspath
from skimage import io
from skimage.segmentation import felzenszwalb
import numpy as np
import math

def scale_invariant_clutter(opt):
    directory = abspath(opt.test_images)
    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    result = []
    for file in files:
        clutter = scale_invariant_clutter_image(file,directory,opt.scale,opt.sigma,opt.submit,opt.save_flag)
        result.append((file,clutter))

    return result

def scale_invariant_clutter_image(path, directory, scale, sigma, output_path, save):
    map = io.imread(join(directory, path))
    segments = felzenszwalb(map, scale, sigma, min_size=5)
    clutter = len(np.unique(segments))/math.pow(scale,-1.32)
    
    return clutter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quad-tree clutter analysis')
    parser.add_argument('--test_images', type=str, default='./data/test_maps', help='path to images to analyse')
    parser.add_argument('--submit', type=str, default='./data/clutter_results', help='path to save results')
    parser.add_argument('--scale', type=float, default=100.0, help='quad tree threshold')
    parser.add_argument('--sigma', type=float, default=0.95, help='sigma value for the Gaussian filter')
    parser.add_argument('--save_flag', type=bool, default=True, help='save clutter maps or not')

    opt = parser.parse_args()

    result = scale_invariant_clutter(opt)
    print(result)