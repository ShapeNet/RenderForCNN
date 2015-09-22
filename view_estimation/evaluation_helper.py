#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *


def viewpoint(img_name_file, class_idx, output_result_file):
    pass
    N = len(open(img_name_file).readlines())

    # use extract_feature to extract to lmdbs
    aaa = 'extract_feature %s %s fc-azimuth,fc-elevation,fc-tilt %s,%s,%s %d lmdb GPU' % ()

    # get probs of azimuth,elevation,tilt of each image, Nx4320
    fc_azimuth=
    fc_elevation=
    fc_tilt=
    
    # use class_name/class_idx to get predictions, Nx1
    pred_azimuth=
    pred_elevation=
    pred_tilt = 

    fout = open(output_result_file, 'w')
    for k in range(N):
        fout.write('%d %d %d\n' % (pred_azimuth[k], pred_elevation[k], pred_tilt[k]))
    fout.close()

# localization + viewpoint estimation
def test_avp_nv(cls_names, img_name_file_list, det_bbox_mat_file_list, result_folder):
    pass
    C = len(cls_names)
    assert(C == len(img_name_file_list))
    assert(C == len(det_bbox_mat_file_list))
    for cls_idx in range(C):
        view_estimation_cmd =  

# viewpoint estimation
def test_vp_acc(img_name_label_file_list, result_folder):
    pass
