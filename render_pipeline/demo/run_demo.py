#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
RENDERING PIPELINE DEMO
run it several times to see random images with different lighting conditions,
viewpoints, truncations and backgrounds.
'''

import os
import sys
from PIL import Image
import random
from datetime import datetime
random.seed(datetime.now())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR,'../'))
sys.path.append(os.path.join(BASE_DIR,'../../'))
from global_variables import *

# set debug mode
debug_mode = 0

if debug_mode:
    io_redirect = ''
else:
    io_redirect = ' > /dev/null 2>&1'

# -------------------------------------------
# RENDER
# -------------------------------------------

# set filepath
syn_images_folder = os.path.join(BASE_DIR, 'demo_images')
model_name = 'chair001'
image_name = 'demo_img.png'
if not os.path.exists(syn_images_folder):
    os.mkdir(syn_images_folder)
    os.mkdir(os.path.join(syn_images_folder, model_name))
viewpoint_samples_file = os.path.join(BASE_DIR, 'sample_viewpoints.txt')
viewpoint_samples = [[float(x) for x in line.rstrip().split(' ')] for line in open(viewpoint_samples_file,'r')]

# run code
v = random.choice(viewpoint_samples)
print ">> Selected view: ", v
python_cmd = 'python %s -a %s -e %s -t %s -d %s -o %s' % (os.path.join(BASE_DIR, 'render_class_view.py'), 
    str(v[0]), str(v[1]), str(v[2]), str(v[3]), os.path.join(syn_images_folder, model_name, image_name))
print ">> Running rendering command: \n \t %s" % (python_cmd)
os.system('%s %s' % (python_cmd, io_redirect))

# show result
print(">> Displaying rendered image ...")
im = Image.open(os.path.join(syn_images_folder, model_name, image_name))
im.show()


# -------------------------------------------
# CROP
# -------------------------------------------

# set filepath
bkg_folder = os.path.join(BASE_DIR, 'sample_bkg_images')
bkg_filelist = os.path.join(bkg_folder, 'filelist.txt')
syn_images_cropped_folder = os.path.join(BASE_DIR, 'demo_images_cropped')
truncation_samples_file = os.path.join(BASE_DIR, 'sample_truncations.txt')

# run matlab code
matlab_cmd = "addpath('%s'); crop_images('%s','%s','%s',1);" % (os.path.dirname(BASE_DIR), syn_images_folder, syn_images_cropped_folder, truncation_samples_file)
print ">> Starting MATLAB ... to run cropping command: \n \t %s" % matlab_cmd
os.system('%s -nodisplay -r "try %s ; catch; end; quit;" %s' % (g_matlab_executable_path, matlab_cmd, io_redirect))

# show result
print(">> Displaying cropped image ...")
im = Image.open(os.path.join(syn_images_cropped_folder, model_name, image_name))
im.show()

 
# -------------------------------------------
# OVERLAY BACKGROUND
# -------------------------------------------

# set filepath
syn_images_cropped_bkg_overlaid_folder = os.path.join(BASE_DIR, 'demo_images_cropped_bkg_overlaid')

# run code
matlab_cmd = "addpath('%s'); overlay_background('%s','%s','%s', '%s', %f, 1);" % (os.path.dirname(BASE_DIR), syn_images_cropped_folder, syn_images_cropped_bkg_overlaid_folder, bkg_filelist, bkg_folder, 1.0)
print ">> Starting MATLAB ... to run background overlaying command: \n \t %s" % matlab_cmd
os.system('%s -nodisplay -r "try %s ; catch; end; quit;" %s' % (g_matlab_executable_path, matlab_cmd, io_redirect))

# show result
print("Displaying background overlaid image ...")
im = Image.open(os.path.join(syn_images_cropped_bkg_overlaid_folder, model_name, image_name.replace('.png', '.jpg')))
im.show()
