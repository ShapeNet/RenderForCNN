#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
sys.path.append(os.path.join(g_render4cnn_root_folder, 'view_estimation'))
from evaluation_helper import viewpoint

if __name__ == '__main__':
    
    img_filenames = [os.path.join(BASE_DIR, 'aeroplane_image.jpg')]
    class_idxs = [g_shape_names.index('aeroplane')]
    output_result_file = os.path.join(BASE_DIR, 'est-view.txt')
    
    if not os.path.exists(output_result_file):
        viewpoint(img_filenames, class_idxs, output_result_file)
 

    # display result by rendering an image of estimated viewpoint
    estimated_viewpoints = [[float(x) for x in line.rstrip().split(' ')] for line in open(output_result_file,'r')]
    v = estimated_viewpoints[0]
    print "Estimated view: ", v
