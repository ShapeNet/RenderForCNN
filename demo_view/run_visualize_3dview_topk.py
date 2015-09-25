#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from PIL import Image
from PIL import ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
sys.path.append(os.path.join(g_render4cnn_root_folder, 'render_pipeline'))

if __name__ == '__main__':
   
    # Feel free to change input image file, result file, and model obj file for rendering

    # -------------------------------- 
    #### CHANGE BEG ####
    output_result_file = os.path.join(BASE_DIR, 'est-view-topk.txt')
    model_obj_file = os.path.join(g_render4cnn_root_folder, 'demo_render', 'sample_model', 'model.obj')
    original_image_file = os.path.join(BASE_DIR, 'chair_image.jpg')
    rendered_image_file_prefix = os.path.join(BASE_DIR, 'chair_in_estimated_view')
    io_redirect = '' #' > /dev/null 2>&1'
    #### CHANGE END ####
    # -------------------------------- 


    # Display estimated viewpoints that are read from result file
    # suppress tilt for chairs
    estimated_viewpoints = [[float(x) for x in line.rstrip().split(' ')] for line in open(output_result_file,'r')]
    v = estimated_viewpoints[0]
    topk = len(v)/4
    print("Estimated views and confidence: ")
    for k in range(topk):
        a,e,t,c = v[4*k : 4*k+4]
        print('rank:%d, confidence:%f, azimuth:%d, elevation:%d' % (k+1, c, a, e))

    # Render images in estimated views        
    for k in range(topk):
        a,e = v[4*k : 4*k+2]
        python_cmd = 'python %s -m %s -a %s -e %s -t %s -d %s -o %s' % (os.path.join(g_render4cnn_root_folder, 'demo_render', 'render_class_view.py'), 
        model_obj_file, str(a), str(e), str(0), str(2.0), rendered_image_file_prefix+str(k)+'.png')
        print ">> Running rendering command: \n \t %s" % (python_cmd)
        os.system('%s %s' % (python_cmd, io_redirect))

     
    print("Show both original aeroplane photo and rendered aeroplane in estimated view:")
    im1 = Image.open(original_image_file)
    im2s = []
    for k in range(topk):
        im2 = Image.open(rendered_image_file_prefix+str(k)+'.png')
        bbox = im2.getbbox()
        im2 = im2.crop(bbox)
        draw = ImageDraw.Draw(im2)
        draw.text((0,0), 'rank: %d, confidence: %f\nazimuth=%f, elevation=%f' % (k+1, v[4*k+3], v[4*k], v[4*k+1]), (0,255,0))
        im2s.append(im2)

    im1.show()
    for k in range(topk):
        im2s[k].show()
