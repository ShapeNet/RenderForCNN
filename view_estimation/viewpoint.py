import numpy as np
import caffe
import os
import math
import argparse
import matplotlib.pyplot as plt
from matplotlib import gridspec
from PIL import Image
import scipy.io
from util import *
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

'''
@auhtor: rqi
@date: aug 10, 2015
@brief: modified from viewpoint.py in Code/3dview
'''

parser = argparse.ArgumentParser(description="3D Viewpoint estimation for rigid object classes in PASCAL VOC.")
parser.add_argument('-i', '--img_filelist', help='Image filename list, each line is absolute path of a cropped image.', required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-c', '--class_idx_file', help='Class idx (0~11) corresponding to imgs.')
parser.add_argument('-o', '--output_filename', help='Filename for output result, each line contains azimuth, elevation, tilt degree.', required=True)
parser.add_argument('-r', '--resize_dim', help='Resize image to square before prediction. (default=256)', default=256, required=False)
parser.add_argument('-g', '--gpu_index', help='GPU index (default=1)', default=1, required=False)
parser.add_argument('--fullview', help='Estimate azimuth, elevation, tilt; otherwize estimate azimuth only.', action='store_true')
args = parser.parse_args()

# COMPUTING OPTIONS
gpu_index = int(args.gpu_index)
BATCH_SIZE = 64

if args.fullview:
  model_deploy_file = g_model_deploy_file_3dview
  model_params_file = g_model_params_file_3dview
  result_keys = g_net_layer_names_3dview #['fc-azimuth', 'fc-elevation', 'fc-tilt']
else:
  model_deploy_file = g_model_deploy_file_azimuth
  model_params_file = g_model_params_file_azimuth
  result_keys = g_net_layer_name_azimuth #_['fc-azimuth']

resize_dim = int(args.resize_dim)
 
# LOAD IMG FILENAMES AND LABELS
img_filenames = [x.rstrip().split(' ')[0] for x in open(args.img_filelist, 'r')]
# LOAD CLASS IDX
try:
  if args.class_name is not None:
      class_idx = g_voc12_rigid_cls_names.index(args.class_name)
      class_idxs = [class_idx for _ in range(len(img_filenames))]
  elif args.class_idx_file is not None:
      class_idxs = [int(line.rstrip()) for line in open(args.class_idx_file,'r')]
except:
  print "Error: cannot find object class %s." % (args.class_name)
  print "Available classes: ", g_voc12_rigid_cls_names

def viewpoint(img_name_file, class_idx, output_result_file):
    gpu_index = 0
    batch_size = 64
    model_params_file = g_caffe_param_file
    model_deploy_file = g_caffe_deploy_file
    result_keys = g_caffe_prob_keys
    resize_dim = g_images_resize_dim
    img_filenames = [x.rstrip().split(' ')[0] for x in open(img_name_file, 'r')]
    
    # ** NETWORK FORWARD PASS **
    probs_lists = batch_predict(gpu_index, batch_size, model_deploy_file, model_params_file, result_keys, img_filenames, resize_dim)
    
    # EXTRACT PRED FROM PROBS
    preds = []
    for k in range(len(result_keys)):
        preds.append([])
    for i in range(len(img_filenames)):
        class_idx = class_idxs[i]
        # pred is the class with highest prob within
        # class_idx*360~class_idx*360+360-1
        # specific to PASCAL3D !!
        #for k in range(3):
        for k in range(len(result_keys)):
            probs = probs_lists[k][i]
            probs = probs[class_idx*360:(class_idx+1)*360]
            pred = probs.argmax() + class_idx*360
            preds[k].append(pred)
    
    # OUTPUT: apred epred tpred
    fout = open(output_result_file, 'w')
    for i in range(len(img_filenames)):
        if args.fullview:
          fout.write('%d %d %d\n' % (preds[0][i] % 360, preds[1][i] % 360, preds[2][i] % 360))
        else:
          fout.write('%d\n' % (preds[0][i] % 360))
    fout.close()
    
    
    # OUTPUT: log file
    log_output_filename = output_result_file+'.log'
    fout = open(log_output_filename, 'w')
    fout.write("img_name_file: %s\nclass_idx: %d\noutput_result_file: %s\nresize_dim: %d\n" % (img_name_file, class_idx, output_result_file, resize_dim))
    fout.write('model_deploy_file_3dview: %s\n' % (model_deploy_file))
    fout.write('model_params_file_3dview: %s\n' % (model_params_file))
    fout.close()
