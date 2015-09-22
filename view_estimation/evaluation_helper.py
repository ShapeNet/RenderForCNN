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

'''
@brief:
    predict 3d viewpoint of object, output prediction results
@input:
    img_filenames - list of image filenames
    class_idxs - list of class index (0~11)
    output_result_file - output views into this file, each line is "<azimuth> <elevation> <tilt>"
@output:
    write 3d viewpoint estimation results to output_result_file
'''
def viewpoint(img_filenames, class_idxs, output_result_file):
    gpu_index = 0
    batch_size = 64
    model_params_file = g_caffe_param_file
    model_deploy_file = g_caffe_deploy_file
    result_keys = g_caffe_prob_keys
    resize_dim = g_images_resize_dim
    image_mean_file = g_image_mean_file
    file_lines = open(img_name_class_file, 'r').readlines()
    
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
    fout.write("output_result_file: %s\nresize_dim: %d\n" % (output_result_file, resize_dim))
    fout.write('model_deploy_file_3dview: %s\n' % (model_deploy_file))
    fout.write('model_params_file_3dview: %s\n' % (model_params_file))
    fout.close()


# localization + viewpoint estimation
def test_avp_nv(cls_names, img_name_file_list, det_bbox_mat_file_list, result_folder):
    C = len(cls_names)
    assert(C == len(img_name_file_list))
    assert(C == len(det_bbox_mat_file_list))
    class_idxs = [g_shape_names.index(name) for name in cls_names]

    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    
    for i,class_idx in enumerate(class_idxs):
        img_filenames = [x.rstrip().split(' ')[0] for x in open(img_name_label_file_list[i]]
        class_idxs = [int(class_idx) for _ in range(len(img_filenames))]
        
        # viewpoint estimation with caffe python
        # wirte <result_folder>/<class_name>_pred_view.txt
        output_result_file = os.path.join(result_folder, cls_names[i]+'_pred_view.txt')
        viewpoint(img_filenames, class_idxs, output_result_file)
   
        # combine det and view
        matlab_cmd = "addpath('%s'); combine_bbox_view('%s','%s','%s','%s', %d);" % (BASE_DIR, cls_names[i], det_bbox_mat_file_list[i], output_result_file, result_folder, 0)
        print matlab_cmd
        os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
    
    # compute AVP-NV for all classes
    matlab_cmd = "addpath('%s'); test_det('%s');" % (BASE_DIR, result_folder)
    print matlab_cmd
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))


# viewpoint estimation
def test_vp_acc(cls_names, img_name_file_list, result_folder, view_label_folder):
    assert(len(cls_names) == len(img_name_file_list))
    class_idxs = [g_shape_names.index(name) for name in cls_names]

    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    
    for i,class_idx in enumerate(class_idxs):
        img_filenames = [x.rstrip().split(' ')[0] for x in open(img_name_label_file_list[i]]
        class_idxs = [int(class_idx) for _ in range(len(img_filenames))]
        
        # viewpoint estimation with caffe python
        # wirte <result_folder>/<class_name>_pred_view.txt
        output_result_file = os.path.join(result_folder, cls_names[i]+'_pred_view.txt')
        viewpoint(img_filenames, class_idxs, output_result_file)
   

    # compute Acc and MedErr
    matlab_cmd = "addpath('%s'); test_gt('%s','%s');" % (BASE_DIR, result_folder, view_label_folder)
    print matlab_cmd
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
