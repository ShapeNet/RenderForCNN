#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import tempfile
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
from caffe_utils import *

def viewpoint(img_name_class_file, output_result_file):
    gpu_index = 0
    batch_size = 64
    model_params_file = g_caffe_param_file
    model_deploy_file = g_caffe_deploy_file
    result_keys = g_caffe_prob_keys
    resize_dim = g_images_resize_dim
    image_mean_file = g_image_mean_file
    file_lines = open(img_name_class_file, 'r').readlines()
    img_filenames = [x.rstrip().split(' ')[0] for x in file_lines]
    class_idxs = [int(x.rstrip().split(' ')[1]) for x in file_lines]
    
    # ** NETWORK FORWARD PASS **
    probs_lists = batch_predict(gpu_index, batch_size, model_deploy_file, model_params_file, result_keys, img_filenames, image_mean_file, resize_dim)
    
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
        fout.write('%d %d %d\n' % (preds[0][i] % 360, preds[1][i] % 360, preds[2][i] % 360))
    fout.close()
    
    
    # OUTPUT: log file
    log_output_filename = output_result_file+'.log'
    fout = open(log_output_filename, 'w')
    fout.write("img_name_class_file: %s\noutput_result_file: %s\nresize_dim: %d\n" % (img_name_class_file, output_result_file, resize_dim))
    fout.write('model_deploy_file_3dview: %s\n' % (model_deploy_file))
    fout.write('model_params_file_3dview: %s\n' % (model_params_file))
    fout.close()


# localization + viewpoint estimation
def test_avp_nv(cls_names, img_name_file_list, det_bbox_mat_file_list, result_folder):
    pass
    C = len(cls_names)
    assert(C == len(img_name_file_list))
    assert(C == len(det_bbox_mat_file_list))
    for cls_idx in range(C):
        pass
        #view_estimation_cmd =  

# viewpoint estimation
def test_vp_acc(img_name_label_file_list, result_folder):
    pass
