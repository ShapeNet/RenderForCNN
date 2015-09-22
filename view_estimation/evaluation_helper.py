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
#from caffe_utils import *

def viewpoint(img_name_file, class_idx, output_result_file):
    N = len(open(img_name_file).readlines())
    print N, math.ceil(N/float(g_test_prototxt_batch_size))

    tmp_azimuth = os.path.join(BASE_DIR, 'tmp_azimuth_lmdb')
    tmp_elevation = os.path.join(BASE_DIR, 'tmp_elevation_lmdb')
    tmp_tilt = os.path.join(BASE_DIR, 'tmp_tilt_lmdb')
    tmp_prototxt_file = os.path.join(BASE_DIR, 'tmp_prototxt_file')
    with open(tmp_prototxt_file, 'w') as fout:
        with open(g_test_prototxt_template_file, 'r') as fin:
            for line in fin:
                fout.write(line.replace('PARAM_IMAGE_LIST_FILE', img_name_file).replace(
                    'PARAM_BATCH_SIZE',str(g_test_prototxt_batch_size)))
    exit()
    # use extract_feature to extract to lmdbs
    try:
        print('Going to extract probs...')
        extract_feature_cmd = 'extract_features %s %s fc-azimuth,fc-elevation,fc-tilt %s,%s,%s %d lmdb GPU' % (g_caffe_param_file, tmp_prototxt_file, tmp_azimuth, tmp_elevation, tmp_tilt, int(math.ceil(N/float(g_test_prototxt_batch_size))))
        print extract_feature_cmd
        os.system(extract_feature_cmd)

        # get probs of azimuth,elevation,tilt of each image, Nx4320
        prob_dim = 4320
        fc_azimuth=load_vector_from_lmdb(tmp_azimuth, prob_dim, N)
        fc_elevation=load_vector_from_lmdb(tmp_elevation, prob_dim, N)
        fc_tilt=load_vector_from_lmdb(tmp_tilt, prob_dim, N)
        
        # use class_name/class_idx to get predictions, Nx1
        pred_azimuth=[argmax(fc_azimuth[k,class_idx*360:(class_idx+1)*360]) for k in range(N)]
        pred_elevation=[argmax(fc_elevation[k,class_idx*360:(class_idx+1)*360]) for k in range(N)]
        pred_tilt=[argmax(fc_tilt[k,class_idx*360:(class_idx+1)*360]) for k in range(N)] 

        fout = open(output_result_file, 'w')
        for k in range(N):
            fout.write('%d %d %d\n' % (pred_azimuth[k], pred_elevation[k], pred_tilt[k]))
        fout.close()
    except:
        pass

    os.system('rm -r %s %s %s %s' % (tmp_azimuth, tmp_elevation, tmp_tilt, tmp_prototxt_file))


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
