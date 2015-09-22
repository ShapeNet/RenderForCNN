#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
g_render4cnn_root_folder = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
g_data_folder = os.path.abspath(os.path.join(g_render4cnn_root_folder, 'data'))
g_datasets_folder = os.path.abspath(os.path.join(g_render4cnn_root_folder, 'datasets'))
g_shapenet_root_folder = os.path.join(g_datasets_folder, 'shapenetcore')
g_pascal3d_root_folder = os.path.join(g_datasets_folder, 'pascal3d')
g_sun2012pascalformat_root_folder = os.path.join(g_datasets_folder, 'sun12pascalformat')

# ------------------------------------------------------------
# RENDER FOR CNN PIPELINE
# ------------------------------------------------------------
g_shape_synset_name_pairs = [('02691156', 'aeroplane'),
                             ('02834778', 'bicycle'),
                             ('02858304', 'boat'),
                             ('02876657', 'bottle'),
                             ('02924116', 'bus'),
                             ('02958343', 'car'),
                             ('03001627', 'chair'),
                             ('04379243', 'diningtable'), #TODO dining?
                             ('03790512', 'motorbike'),
                             ('04256520', 'sofa'),
                             ('04468005', 'train'),
                             ('03211117', 'tvmonitor')]
g_shape_synsets = [x[0] for x in g_shape_synset_name_pairs]
g_shape_names = [x[1] for x in g_shape_synset_name_pairs]
g_syn_images_folder = os.path.join(g_data_folder, 'syn_images')
g_syn_images_cropped_folder = os.path.join(g_data_folder, 'syn_images_cropped')
g_syn_images_bkg_overlaid_folder = os.path.join(g_data_folder, 'syn_images_cropped_bkg_overlaid')
g_syn_bkg_filelist = os.path.join(g_sun2012pascalformat_root_folder, 'filelist.txt')
g_syn_bkg_folder = os.path.join(g_sun2012pascalformat_root_folder, 'JPEGImages')
g_syn_cluttered_bkg_ratio = 0.8
g_blender_executable_path = '/orions-zfs/software/blender-2.71/blender'
g_matlab_executable_path = '/orions3-zfs/software/matlab2014b/bin/matlab'
g_blank_blend_file_path = os.path.join(g_render4cnn_root_folder, 'render_pipeline/blank.blend') 
g_syn_images_num_per_category = 200000
g_syn_rendering_thread_num = 20

# Skip orions3 since model is store on orions3
g_hostname_synset_idx_map = {'oriong.stanford.edu': [0,1],
                             'orionp.stanford.edu': [2,3,4],
                             'orionp2.stanford.edu': [5,6,7],
                             'orions2.stanford.edu':[8,9], 
                             'orions4.stanford.edu':[10,11]}
# Crop and overlay is IO-heavy, running on local FS is much faster
g_crop_hostname_synset_idx_map = {'orions4.stanford.edu': range(12)}
g_overlay_hostname_synset_idx_map = {'orions4.stanford.edu': range(12)}

# view and truncation distribution estimation
g_matlab_kde_folder = '/orions-zfs/software/matlab-package/kde'
g_view_statistics_folder = os.path.join(g_data_folder, 'view_statistics')
g_view_distribution_folder = os.path.join(g_data_folder, 'view_distribution')
g_view_distribution_files = dict(zip(g_shape_synsets, [os.path.join(g_view_distribution_folder, name+'.txt') for name in g_shape_names]))
g_truncation_statistics_folder = os.path.join(g_data_folder, 'truncation_statistics')
g_truncation_distribution_folder = os.path.join(g_data_folder, 'truncation_distribution')
g_truncation_distribution_files = dict(zip(g_shape_synsets, [os.path.join(g_truncation_distribution_folder, name+'.txt') for name in g_shape_names]))

# render_model_views
g_syn_light_num_lowbound = 0
g_syn_light_num_highbound = 6
g_syn_light_dist_lowbound = 8
g_syn_light_dist_highbound = 20



# ------------------------------------------------------------
# VIEW_ESTIMATION
# ------------------------------------------------------------
g_syn_images_lmdb_folder = os.path.join(g_data_folder, 'syn_lmdbs')
g_syn_images_lmdb_pathname_prefix = '/ShapeNetDL/projects/render4cnn/syn_lmdb' #os.path.join(g_syn_images_lmdb_folder, 'syn_lmdb')
g_syn_images_resize_dim = 227
g_images_resize_dim = 227

g_real_images_folder = os.path.join(g_data_folder, 'real_images')
g_real_images_voc12val_det_bbox_folder = os.path.join(g_real_images_folder, 'voc12val_det_bbox')
g_real_images_voc12val_easy_gt_bbox_folder = os.path.join(g_real_images_folder, 'voc12val_easy_gt_bbox')
g_real_images_voc12train_all_gt_bbox_folder = os.path.join(g_real_images_folder, 'voc12train_all_gt_bbox')
g_real_images_voc12train_flip = 1
g_real_images_voc12train_aug_n = 1
g_real_images_voc12train_jitter_IoU = 1
g_real_images_lmdb_folder = os.path.join(g_data_folder, 'real_lmdbs')
g_real_images_voc12train_all_gt_bbox_lmdb_prefix = os.path.join(g_real_images_lmdb_folder, 'voc12train_all_gt_bbox_lmdb')

g_detection_results_folder = os.path.join(g_data_folder, 'detection_results')
g_rcnn_detection_bbox_mat_filelist = os.path.join(g_detection_results_folder, 'bbox_mat_filelist.txt')

g_rcnn_caffe_model = '/orions3-zfs/projects/haosu/Image2Scene/data/pretrained_models/rcnn.caffemodel'
