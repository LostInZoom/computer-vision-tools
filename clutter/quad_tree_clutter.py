import argparse
from os import listdir
from os.path import isfile, join, abspath
from skimage import io, img_as_ubyte
from skimage.filters import gaussian
from skimage.color import rgb2gray
from quad_tree_leaf import quad_tree_leaf
import cv2
from pathlib import Path
import math

def quad_tree_clutter(opt):
    directory = abspath(opt.test_images)
    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    result = []
    for file in files:
        print(file)
        clutter = quad_tree_clutter_image(file,directory,opt.threshold,opt.sigma,opt.submit,opt.save_flag,opt.heatmap)
        result.append((file,clutter))

    return result

def quad_tree_clutter_image(path, directory, threshold, sigma, output_path, save, heatmap):
    map = io.imread(join(directory, path))
    grayscale = rgb2gray(map)
    smoothed = gaussian(grayscale,sigma)
    height = smoothed.shape[0]
    width = smoothed.shape[1]
    root = quad_tree_leaf(0,0,height,width,smoothed,None)
    quadtree= compute_quad_tree(root,threshold)
    print(len(quadtree))

    if(save==True):
        # create clutter image
        clutter_map = io.imread(join(directory, path))
        for leaf in quadtree:
            if(leaf.hasChild()==False):
                cv2.rectangle(clutter_map,(leaf.column1,leaf.line1),(leaf.column1+leaf.leaf_width,leaf.line1+leaf.leaf_height),(0,0,0))
        # create file path
        filename = Path(path).stem +'_clutter.png'
        filepath = join(output_path,filename)
        # save image
        io.imsave(filepath,clutter_map)

    if(heatmap==True):
        heatmap = rgb2gray(io.imread(join(directory, path)))
        x = smoothed.shape[0]
        y = smoothed.shape[1]
        maxshape = max(x,y)
        for leaf in quadtree:
            if(leaf.hasChild()==False):
                for i in range(leaf.line1,leaf.line1+leaf.leaf_height):
                    for j in range(leaf.column1,leaf.column1+leaf.leaf_width):
                        heatmap[i,j] = math.floor(256*leaf.depth/(maxshape*0.5))
        # create file path
        filename = Path(path).stem +'_clutter_heatmap.png'
        filepath = join(output_path,filename)
        # save image
        io.imsave(filepath,heatmap)

    # compute clutter value
    clutter = 0
    for leaf in quadtree:
        if(leaf.hasChild()==False):
            clutter += 1
    
    return (clutter-1)/(width*height)

def compute_quad_tree(root,threshold):
    leaves= []
    leaves.append(root)
    stack = []
    stack.append(root)
    while(len(stack)!=0):
        leaf = stack.pop()
        divide_leaf(leaf,leaves,stack,threshold)

    return leaves

def divide_leaf(leaf, leaves, stack, threshold):
    divided=False
    for col in range(leaf.column1+1,leaf.column1+leaf.leaf_width-1):
        for line in range(leaf.line1+1,leaf.line1+leaf.leaf_height-1):
            # check if pixel (col,line) is different from its neighbours
            pixel = leaf.initial_image[line,col]
            left = leaf.initial_image[line,col-1]
            right = leaf.initial_image[line,col+1]
            above = leaf.initial_image[line-1,col]
            below = leaf.initial_image[line+1,col]
            if (abs(pixel-left)>threshold) or (abs(pixel-right)>threshold) or (abs(pixel-below)>threshold) or (abs(pixel-above)>threshold):
                # create four new leaves
                width = math.floor(leaf.leaf_width/2)
                height = math.floor(leaf.leaf_height/2)
                leaf1 = quad_tree_leaf(leaf.line1,leaf.column1, height, width, leaf.initial_image, leaf)
                leaf2 = quad_tree_leaf(leaf.line1+height, leaf.column1, height, width, leaf.initial_image, leaf)
                leaf3 = quad_tree_leaf(leaf.line1,leaf.column1 + width, height, width, leaf.initial_image, leaf)
                leaf4 = quad_tree_leaf(leaf.line1 + height,leaf.column1 + width, height, width, leaf.initial_image, leaf)
                # update the list of leaves
                leaves.append(leaf1)
                leaves.append(leaf2)
                leaves.append(leaf3)
                leaves.append(leaf4)
                # put the new leaves in the stack
                stack.append(leaf1)
                stack.append(leaf2)
                stack.append(leaf3)
                stack.append(leaf4)
                divided = True
                break
        
        if(divided==True):
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quad-tree clutter analysis')
    parser.add_argument('--test_images', type=str, default='./data/test_maps', help='path to images to analyse')
    parser.add_argument('--submit', type=str, default='./data/clutter_results', help='path to save results')
    parser.add_argument('--threshold', type=float, default=0.03, help='quad tree threshold')
    parser.add_argument('--sigma', type=float, default=0.3, help='sigma value for the Gaussian filter')
    parser.add_argument('--save_flag', type=bool, default=True, help='save clutter maps or not')
    parser.add_argument('--heatmap', type=bool, default=True, help='save clutter heatmaps or not')

    opt = parser.parse_args()

    result = quad_tree_clutter(opt)
    print(result)