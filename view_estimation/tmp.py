from evaluation_helper import *

img_name_file = '../data/real_images/voc12val_easy_gt_bbox/chair.txt'

img_filenames = [x.rstrip().split(' ')[0] for x in open(img_name_file)]
class_idxs = [int(class_idx) for _ in range(len(img_filenames))]

viewpoint(img_filenames, class_idxs,'chair_preds.txt')
