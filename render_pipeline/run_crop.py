#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
CROP_ALL_IMAGES
@brief:
    crop all rendered images of PASCAL3D 12 rigid object classes
'''

import os
import sys
import socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

if __name__ == '__main__':
    if not os.path.exists(g_syn_images_cropped_folder):
        os.mkdir(g_syn_images_cropped_folder) 
    
    for idx in g_crop_hostname_synset_idx_map[socket.gethostname()]:
        synset = g_shape_synsets[idx]
        name = g_shape_names[idx]
        print('%d: %s, %s\n' % (idx, synset, name))
        matlab_cmd = "addpath('%s'); crop_images('%s','%s','%s');" % (BASE_DIR, os.path.join(g_syn_images_folder, synset), os.path.join(g_syn_images_cropped_folder, synset), os.path.join(g_truncation_distribution_folder, name+'.txt'))
        print matlab_cmd
        os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
