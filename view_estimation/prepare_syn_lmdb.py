#!/usr/bin/python

# prepare filelist for syn images

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

if __name__ == '__main__':

    # get image filenames and labels, separated to train/test sets
    for idx, synset in enumerate(g_shape_synsets):
        name = g_shape_names[idx]
        get_one_category_filelist(synset, os.path.join(g_syn_images_lmdb_folder, name+'_train.txt'), os.path.join(g_syn_images_lmdb_folder, name+'_test.txt'))

    for keyword in ['train', 'test']:
        # combine filenames&labels from all 12 classes (shuffled)
        input_file_list = [os.path.join(g_syn_images_lmdb_folder, '%s_%s.txt' % (name, keyword)) for name in g_shape_names]
        output_file = os.path.join(g_syn_images_lmdb_folder, 'all_%s.txt' % (keyword))
        combine_files(input_file_list, output_file)
        
        # generate LMDB
        generate_image_view_lmdb(output_file, g_syn_images_lmdb_pathname_prefix, g_syn_images_resize_dim)
