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
g_sun2012pascalformat_root_folder = os.path.join(g_datasets_folder, 'sun2012pascalformat')

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
g_blender_executable_path = '/orions-zfs/software/blender-2.71/blender'
g_blank_blend_file_path = os.path.join(g_render4cnn_root_folder, 'render_pipeline/blank.blend') 
g_syn_images_num_per_category = 200000
g_syn_rendering_thread_num = 20

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
