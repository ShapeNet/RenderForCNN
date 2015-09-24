import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
from evaluation_helper import *

cls_names = g_shape_names

img_name_file_list = [os.path.join(g_real_images_voc12val_det_bbox_folder, name+'.txt') for name in cls_names]
det_bbox_mat_file_list = [os.path.join(g_detection_results_folder, x.rstrip()) for x in open(g_rcnn_detection_bbox_mat_filelist)]
result_folder = os.path.join(BASE_DIR, 'avp_test_results')
test_avp_nv(cls_names, img_name_file_list, det_bbox_mat_file_list, result_folder)

img_name_file_list = [os.path.join(g_real_images_voc12val_easy_gt_bbox_folder, name+'.txt') for name in cls_names]
view_label_folder = g_real_images_voc12val_easy_gt_bbox_folder
result_folder = os.path.join(BASE_DIR, 'vp_test_results')
test_vp_acc(cls_names, img_name_file_list, result_folder, view_label_folder)
