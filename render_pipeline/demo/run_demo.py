#!/usr/bin/python

import os
import sys

BASE_DIR = os.path.dirname(__file__)

os.system('python %s' % (os.path.join(BASE_DIR, 'render_class_view.py')))

print "Rendered image:"
from PIL import Image
im = Image.open(os.path.join(BASE_DIR, 'demo_img.png'))
im.show()
