import os
from global_variables import *

# matlab global variable file
mf = open(os.path.join(g_render4cnn_root_folder, 'global_variables.m'), 'w')

mf.write("g_matlab_kde_folder = '%s';\n" % (g_matlab_kde_folder))
mf.write("g_view_statistics_folder = '%s';\n" % (g_view_statistics_folder))
mf.write("g_view_distribution_folder = '%s';\n" % (g_view_distribution_folder))
mf.write("g_truncation_statistics_folder = '%s';\n" % (g_truncation_statistics_folder))
mf.write("g_truncation_distribution_folder = '%s';\n" % (g_truncation_distribution_folder))

mf.write("g_pascal3d_root_folder = '%s';\n" % (g_pascal3d_root_folder))

mf.write("g_cls_names = {'aeroplane','bicycle','boat','bottle','bus','car','chair','diningtable','motorbike','sofa','train','tvmonitor'};\n")
mf.write("g_detection_results_folder = '%s';\n" % (g_detection_results_folder))
