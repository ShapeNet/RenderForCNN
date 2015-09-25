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
    predict 3d viewpoint of object, output prediction results (compatible with NEW caffe interface - 2015 Aug)
@input:
    img_filenames - list of image filenames
    class_idxs - list of class index (0~11)
    output_result_file - output views into this file, each line is "<azimuth> <elevation> <tilt>"
@output:
    write 3d viewpoint estimation results to output_result_file
'''
def viewpoint(img_filenames, class_idxs, output_result_file):
    batch_size = g_test_batch_size
    model_params_file = g_caffe_param_file
    model_deploy_file = g_caffe_deploy_file
    result_keys = g_caffe_prob_keys
    resize_dim = g_images_resize_dim
    image_mean_file = g_image_mean_file
    
    # ** NETWORK FORWARD PASS **
    probs_lists = batch_predict(model_deploy_file, model_params_file, batch_size, result_keys, img_filenames, image_mean_file, resize_dim)
    
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


'''
@brief:
    get local maximums from an 1-D array of angles (e.g. if len(prob)=360 then 0==360)
@input: 
    prob: N*1 array
    num_bin: local area width
    diff_threshold: regard close preds as duplicates
@output: 
    preds_list: a list of (pred,prob-for-the-pred) tuples 
'''
def get_top_preds(prob, num_bin=8, diff_threshold=10):
    N = len(prob)
    bin_width = N/num_bin
    preds_list = [] # list of tuples of (<pred>, <prob-of-the-pred>)
    preds_list.append((prob.argmax(), max(prob)))

    for i in range(0,num_bin):
        # get local top pred
        prob_bin = prob[i*bin_width : (i+1)*bin_width]
        local_pred = prob_bin.argmax() + i*bin_width
        local_prob = max(prob_bin)

        # verify
        duplicate = 0
        for i, ituple in enumerate(preds_list):
            ipred, iprob = ituple
            if min(abs(local_pred - ipred), N - abs(local_pred - ipred)) < diff_threshold:
                if local_prob > iprob:
                    preds_list[i] = (local_pred, local_prob) # exchange to bigger one
                duplicate = 1 # too close to existed pred
                break
        if duplicate == 0:
            preds_list.append((local_pred, local_prob))
    preds_list = sorted(preds_list, key=lambda item:item[1], reverse=True)
    return preds_list



'''
@brief:
    get topk confident viewpoint predictions from probs
@input:
    probs_3dview - a length-3 list of azimuth, elevation and tilt probs (each is length-360 list)
    topk (K) - integer (K>=1). only return top K confident result
@output:
    return topk_viewpoints - a length-topk list of tuples of (<viewpoint-tuple>, <confidence>), where
    <viewpoint-tuple> is a length-3 tuples of azimuth, elevation and tilt angles in degree
'''
def get_topk_viewpoints(probs_3dview, topk):
    assert(topk>=1)
    viewpoints_list = []

    # secure softmax. used to normalize an array to 0~1 with sum as 1
    def my_softmax(x):
        ex = np.exp(x - np.max(x))
        out = ex / ex.sum()
        return out

    # Rank by prob-azimuth * prob-elevation * prob-tilt
    #for n in range(10):
    #    if n*n*n >= topk: break
    #probs_3dview = [my_softmax(prob) for prob in probs_3dview]
    #preds_list_azimuth = get_top_preds(probs_3dview[0], 16, 45)[0:n]
    #preds_list_elevation = get_top_preds(probs_3dview[1], 24, 10)[0:n]
    #preds_list_tilt = get_top_preds(probs_3dview[2], 36, 5)[0:n]
    #for i in range(n):
    #    for j in range(n):
    #        for k in range(n):
    #            apred,aprob = preds_list_azimuth[i]
    #            epred,eprob = preds_list_elevation[j]
    #            tpred,tprob = preds_list_tilt[k]
    #            viewpoints_list.append(((apred,epred,tpred), np.log(aprob)+np.log(eprob)+np.log(tprob)))
    
    # Rank by azimuth and a bit of elevation
    preds_list_azimuth = get_top_preds(probs_3dview[0], 16, 45)
    for i in range(min(topk,len(preds_list_azimuth))):
        apred,aprob = preds_list_azimuth[i]
        viewpoints_list.append(((apred, probs_3dview[1].argmax(), probs_3dview[2].argmax()), aprob))
        

    viewpoints_list = sorted(viewpoints_list, key=lambda item:item[1], reverse=True)
    topk_viewpoints = viewpoints_list[0:topk]

    return topk_viewpoints
    


'''
@brief:
    predict 3d viewpoint of object, output **TOP-k** prediction results (compatible with NEW caffe interface - 2015 Aug)
@input:
    img_filenames - list of image filenames
    class_idxs - list of class index (0~11)
    topk (K) - integer number (10=>K>=1). choose top K prediction results (in default, set to 1)
    output_result_file - string. output estimated viewpoints into this file
@output:
    return preds - a lenght-len(img_filenames) list of length-topk list of tuples 
        of (<viewpoint-tuple>, <confidence>), ranked by confidence (high to low),
        where <viewpoint-tuple> is a length-3 tuple of azimuth, elevation, tilt angles in degree

        e.g. for len(img_filenames)=3 and topk=2, preds is like
            [ [((a,e,t),c),((a,e,t),c)], 
              [((a,e,t),c),((a,e,t),c)], 
              [((a,e,t),c),((a,e,t),c)] ]

    if output_result_file is not None
        write 3d viewpoint estimation results to output_result_file, each line has Kx(3+1) numbers as 
        "<azimuth-top1> <elevation-top1> <tilt-top1> <confidence-top1> <azimuth-top2> <elevation-top2> <tilt-top2> <confidence-top2> ..."
        write output log file to <output_result_file>.log
'''
def viewpoint_topk(img_filenames, class_idxs, topk=1, output_result_file=None):
    batch_size = g_test_batch_size
    model_params_file = g_caffe_param_file
    model_deploy_file = g_caffe_deploy_file
    result_keys = g_caffe_prob_keys
    resize_dim = g_images_resize_dim
    image_mean_file = g_image_mean_file
    assert(topk>=1 and topk<=10) # from 1^3 to 10^3
    assert(len(result_keys) == 3) #azimuth,elevation,tilt
    
    # ** NETWORK FORWARD PASS **
    probs_lists = batch_predict(model_deploy_file, model_params_file, batch_size, result_keys, img_filenames, image_mean_file, resize_dim)
    
    # EXTRACT PRED FROM PROBS
    preds = []
    for k in range(len(img_filenames)):
        preds.append([])
    for i in range(len(img_filenames)):
        class_idx = class_idxs[i]

        # probs_3dview is length-3 list of azimuth, elevation and tilt probs (each is length-360 list)
        probs_3dview = [] 
        for k in range(len(result_keys)):
            # probs for class_idx:
            # class_idx*360~class_idx*360+360-1
            probs = probs_lists[k][i]
            probs = probs[class_idx*360:(class_idx+1)*360]
            probs_3dview.append(probs)
       
        # get topk viewpoints: length-topk list of lenght-3 tuples
        topk_viewpoints = get_topk_viewpoints(probs_3dview, topk)
        preds[i] = topk_viewpoints
    
    if output_result_file is not None:
        # OUTPUT: apred epred tpred
        fout = open(output_result_file, 'w')
        for i in range(len(img_filenames)):
            topk_views = preds[i] 
            for k in range(len(topk_views)):
                va,ve,vt = topk_views[k][0]
                confidence = topk_views[k][1]
                fout.write('%d %d %d %f ' % (va,ve,vt,confidence))
            fout.write('\n')
        fout.close()
        
        
        # OUTPUT: log file
        log_output_filename = output_result_file+'.log'
        fout = open(log_output_filename, 'w')
        fout.write("output_result_file: %s\nresize_dim: %d\ntopk: %d\n" % 
                (output_result_file, resize_dim, topk))
        fout.write('model_deploy_file_3dview: %s\n' % (model_deploy_file))
        fout.write('model_params_file_3dview: %s\n' % (model_params_file))
        fout.close()

    return preds

'''
@brief:
    evaluation of joint localization and viewpoint estimation (azimuth only)
    metric is AVP-NV
@input:
    cls_names - a list of strings of PASCAL3D class names
    img_name_file_list - a list of filenames of images to be evaluated
    det_bbox_mat_file_list - a list of det bbox file (contains boxes of Nx5, see combine_bbox_view.m for more)
    result_folder - result .mat files will be saved there
@output:
    output .mat results (see combine_bbox_view.m for more details) into result_folder.
    display AVP-NV results 
@dependency:
    combine_bbox_view.m (output <clsname>_v<NV>.mat like chair_v8.mat)
    test_det.m  (assumes .mat files available in folder)
'''
def test_avp_nv(cls_names, img_name_file_list, det_bbox_mat_file_list, result_folder):
    C = len(cls_names)
    assert(C == len(img_name_file_list))
    assert(C == len(det_bbox_mat_file_list))
    class_idxs = [g_shape_names.index(name) for name in cls_names]

    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    
    for i,class_idx in enumerate(class_idxs):
        img_filenames = [x.rstrip().split(' ')[0] for x in open(img_name_file_list[i])]
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


'''
@brief:
    evaluation of 3D viewpoint estimation accuracy
    metric is Acc-pi/6 and MedErr
@input:
    cls_names - a list of strings of PASCAL3D class names
    img_name_file_list - a list of filenames of images to be evaluated
    result_folder - result view estimation .txt files will be saved there
    view_label_folder - assumes dir structure of <view_label_folder>/<classname>.txt each file containing <imgpath> <clsidx> <azimuth> <tilt> labels
@output:
    output 3D viewpoint estimation results into result_folder
    display Acc and MedErr results
@dependency:
    test_gt.m (assumes <clsname>_pred_view.txt available in folder)
'''
def test_vp_acc(cls_names, img_name_file_list, result_folder, view_label_folder):
    assert(len(cls_names) == len(img_name_file_list))
    class_idxs = [g_shape_names.index(name) for name in cls_names]

    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    
    for i,class_idx in enumerate(class_idxs):
        tmp_img_filenames = [x.rstrip().split(' ')[0] for x in open(img_name_file_list[i])]
        tmp_class_idxs = [int(class_idx) for _ in range(len(tmp_img_filenames))]
        
        # viewpoint estimation with caffe python
        # wirte <result_folder>/<class_name>_pred_view.txt
        output_result_file = os.path.join(result_folder, cls_names[i]+'_pred_view.txt')
        viewpoint(tmp_img_filenames, tmp_class_idxs, output_result_file)
   

    # compute Acc and MedErr
    matlab_cmd = "addpath('%s'); test_gt('%s','%s');" % (BASE_DIR, result_folder, view_label_folder)
    print matlab_cmd
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
