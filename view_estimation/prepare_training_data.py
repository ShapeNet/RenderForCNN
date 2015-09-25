#!/usr/bin/python

'''
Prepare Training Data

Running this program will populate following folders:
  g_syn_images_lmdb_folder
    with img-label files and g_syn_images_lmdb_pathname_prefix+[_label,_image] LMDBs
  g_real_images_voc12train_all_gt_bbox_folder
    with cropped images and img-label files and g_real_images_voc12train_all_gt_bbox_lmdb_prefix+[_label,_image] LMDBs
'''

import os
import sys
from data_prep_helper import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

if __name__ == '__main__':

    # ----------------------------------
    # ---- SYNTHESIZED IMAGES ----------
    # ----------------------------------

    if not os.path.exists(g_syn_images_lmdb_folder):
        os.mkdir(g_syn_images_lmdb_folder)

    # get image filenames and labels, separated to train/test sets
    for idx, synset in enumerate(g_shape_synsets):
        name = g_shape_names[idx]
        get_one_category_image_label_file(synset, os.path.join(g_syn_images_lmdb_folder, name+'_train.txt'), os.path.join(g_syn_images_lmdb_folder, name+'_test.txt'))

    for keyword in ['train', 'test']:
        # combine filenames&labels from all 12 classes (shuffled)
        input_file_list = [os.path.join(g_syn_images_lmdb_folder, '%s_%s.txt' % (name, keyword)) for name in g_shape_names]
        output_file = os.path.join(g_syn_images_lmdb_folder, 'all_%s.txt' % (keyword))
        combine_files(input_file_list, output_file)
        
        # generate LMDB
        generate_image_view_lmdb(output_file, '%s_%s' % (g_syn_images_lmdb_pathname_prefix, keyword))

    
    # ----------------------------------
    # ---- VOC12 TRAIN SET -------------
    # ----------------------------------

    # prepare voc12train gt bbox images and its LMDB
    matlab_cmd = "addpath('%s'); prepare_voc12_imgs('train','%s',struct('flip',%d,'aug_n',%d,'jitter_IoU',%d,'difficult',1,'truncated',1,'occluded',1));" % (BASE_DIR, g_real_images_voc12train_all_gt_bbox_folder, g_real_images_voc12train_flip, g_real_images_voc12train_aug_n, g_real_images_voc12train_jitter_IoU)
    print matlab_cmd
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))

    if not os.path.exists(g_real_images_lmdb_folder):
        os.mkdir(g_real_images_lmdb_folder)
    
    # generate lmdb
    input_file_list = [os.path.join(g_real_images_voc12train_all_gt_bbox_folder,name+'.txt') for name in g_shape_names]
    output_file = os.path.join(g_real_images_voc12train_all_gt_bbox_folder, 'all.txt')
    combine_files(input_file_list, output_file)
    generate_image_view_lmdb(output_file, g_real_images_voc12train_all_gt_bbox_lmdb_prefix)
