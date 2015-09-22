#!/usr/bin/python

'''
prepare filelist and LMDB for real images
running this program will populate following folders:
  g_real_images_voc12val_det_bbox_folder
  g_real_images_voc12val_easy_gt_bbox_folder
  g_real_images_voc12train_all_gt_bbox_folder
with cropped images and img-[label] files
and 
  g_real_images_voc12train_all_gt_bbox_lmdb_prefix+[_label,_image]
with lmdbs
'''

import os
import sys
from data_prep_helper import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

if __name__ == '__main__':
    
    # prepare voc12val det bbox (from rcnn) images
    matlab_cmd = "addpath('%s'); prepare_voc12val_det_imgs('%s','%s', 0);" % (BASE_DIR, g_real_images_voc12val_det_bbox_folder, g_rcnn_detection_bbox_mat_filelist)
    print matlab_cmd
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
   

    # prepare voc12val gt bbox easy (no trunction/occlusion) images
    matlab_cmd = "addpath('%s'); prepare_voc12_imgs('val','%s',struct('flip',0,'aug_n',1,'jitter_IoU',1,'difficult',0,'truncated',0,'occluded',0));" % (BASE_DIR, g_real_images_voc12val_easy_gt_bbox_folder)
    print matlab_cmd
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
   

    # prepare voc12train gt bbox images and its LMDB
    matlab_cmd = "addpath('%s'); prepare_voc12_imgs('train','%s',struct('flip',%d,'aug_n',%d,'jitter_IoU',%d,'difficult',1,'truncated',1,'occluded',1));" % (BASE_DIR, g_real_images_voc12train_all_gt_bbox_folder, g_real_images_voc12train_flip, g_real_images_voc12train_aug_n, g_real_images_voc12train_jitter_IoU)
    print matlab_cmd
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))

    if not os.path.exists(g_real_images_lmdb_folder):
        os.mkdir(g_real_images_lmdb_folder)

    input_file_list = [os.path.join(g_real_images_voc12train_all_gt_bbox_folder,name+'.txt') for name in g_shape_names]
    output_file = os.path.join(g_real_images_voc12train_all_gt_bbox_folder, 'all.txt')
    combine_files(input_file_list, output_file)
    generate_image_view_lmdb(output_file, g_real_images_voc12train_all_gt_bbox_lmdb_prefix, g_images_resize_dim)
