#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
sys.path.append(os.path.join(g_render4cnn_root_folder, 'render_pipeline'))

if __name__ == '__main__':
    
    img_filenames = [os.path.join(BASE_DIR, 'aeroplane_image.jpg')]
    class_idxs = [g_shape_names.index('aeroplane')]
    output_result_file = os.path.join(BASE_DIR, 'est-view.txt')
    
    # display result by rendering an image of estimated viewpoint
    estimated_viewpoints = [[float(x) for x in line.rstrip().split(' ')] for line in open(output_result_file,'r')]
    v = estimated_viewpoints[0]
    print "Estimated view: ", v

    render_demo_folder = os.path.join(g_render4cnn_root_folder, 'demo_render')
    # Change the model.obj file to render images of a diferrent model/category
    aeroplane_model = os.path.join(render_demo_folder, 'sample_model2', 'model.obj')
    output_image = os.path.join(BASE_DIR, 'aeroplane_in_estimated_view.png')
    io_redirect = '' #' > /dev/null 2>&1'
            
    python_cmd = 'python %s -m %s -a %s -e %s -t %s -d %s -o %s' % (os.path.join(render_demo_folder, 'render_class_view.py'), 
        aeroplane_model, str(v[0]), str(v[1]), str(v[2]), str(1.0), output_image)
    print ">> Running rendering command: \n \t %s" % (python_cmd)
    os.system('%s %s' % (python_cmd, io_redirect))

    
    print("Show both original aeroplane photo and rendered aeroplane in estimated view:")
    im1 = Image.open(img_filenames[0])
    im2 = Image.open(output_image)
    bbox = im2.getbbox()
    im2 = im2.crop(bbox)

    im1.show()
    im2.show()
