#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
BACKGROUND OVERLAY
@brief:
    overlay backgrounds to images of PASCAL3D 12 rigid object classes
'''

import os
import sys
import socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

if __name__ == '__main__':
    if not os.path.exists(g_syn_images_bkg_overlaid_folder):
        os.mkdir(g_syn_images_bkg_overlaid_folder) 
    
    for idx in g_overlay_hostname_synset_idx_map[socket.gethostname()]:
        synset = g_shape_synsets[idx]
        print('%d: %s, %s\n' % (idx, synset, g_shape_names[idx]))
        matlab_cmd = "addpath('%s'); overlay_background('%s','%s','%s', '%s', %f);" % (BASE_DIR, os.path.join(g_syn_images_cropped_folder, synset), os.path.join(g_syn_images_bkg_overlaid_folder, synset), g_syn_bkg_filelist, g_syn_bkg_folder, g_syn_cluttered_bkg_ratio)
        print matlab_cmd
        os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
