#!/usr/bin/python

import os.path as osp
import sys
import argparse
import os, tempfile, glob, shutil

BASE_DIR = osp.dirname(__file__)
sys.path.append(osp.join(BASE_DIR,'../'))
from global_variables import *


parser = argparse.ArgumentParser(description='Render Model Images of a certain class and view')
parser.add_argument('-m', '--model_file', help='CAD Model obj filename', default=osp.join(BASE_DIR,'sample_model/model.obj'))
parser.add_argument('-a', '--azimuth', default='45')
parser.add_argument('-e', '--elevation', default='20')
parser.add_argument('-t', '--tilt', default='0')
parser.add_argument('-d', '--distance', default='2.0')
parser.add_argument('-o', '--output_img', help='Output img filename.', default=osp.join(BASE_DIR, 'demo_img.png')) 
args = parser.parse_args()

blank_file = osp.join(g_blank_blend_file_path)
render_code = osp.join(g_render4cnn_root_folder, 'render_pipeline/render_model_views.py')

# MK TEMP DIR
temp_dirname = tempfile.mkdtemp()
view_file = osp.join(temp_dirname, 'view.txt')
view_fout = open(view_file,'w')
view_fout.write(' '.join([args.azimuth, args.elevation, args.tilt, args.distance]))
view_fout.close()

try:
    render_cmd = '%s %s --background --python %s -- %s %s %s %s %s' % (g_blender_executable_path, blank_file, render_code, args.model_file, 'xxx', 'xxx', view_file, temp_dirname)
    print render_cmd
    os.system(render_cmd)
    imgs = glob.glob(temp_dirname+'/*.png')
    shutil.move(imgs[0], args.output_img)
except:
    print('render failed. render_cmd: %s' % (render_cmd))

# CLEAN UP
shutil.rmtree(temp_dirname)
